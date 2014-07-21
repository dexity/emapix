import StringIO
from PIL import Image
import threading
import Queue

from emapix.utils import amazon_s3 as storage
from emapix.utils.utils import storage_filename
from emapix.utils.const import IMAGE_FORMATS
import logging


def crop_s3_image(img_name, crop_name, select_box):
    """
    img_name    - S3 key of the preview image
    crop_name   - S3 key of the crop image
    select_box  - tuple of left upper corner coordinates, widht and height
    
    Returns tuple (status, file_size)
    """
    (x, y, w, h)    = select_box
    try:
        # Download selected image from Amazon S3
        fd  = StringIO.StringIO()
        content_type    = storage.download_file(fd, img_name)
        im1     = Image.open(fd)
        im2     = im1.crop((x, y, x + w, y + h))    # lazy operation
        fd.close()
        
        # Upload cropped image to Amazon S3
        fd      = StringIO.StringIO()
        im2.save(fd, im1.format)
        # Get file size
        fd.seek(0, 2)   # End of file
        size    = fd.tell()
        
        # Upload the image to Amazon S3
        fd.seek(0)  # Beginning of file
        status  = storage.upload_file(fd, crop_name, content_type)
        return (status, size)
    except Exception, e:
        logging.error(str(e))
        return (False, 0)


def load_s3image(file_base, format):
    "Download cropped file from S3 and return Image object of the file"
    filename    = storage_filename(file_base, "crop", format)
    fd  = StringIO.StringIO()
    content_type = storage.download_file(fd, filename)
    return Image.open(fd)


def proc_images(file_base, db_imgs, format):
    "Processes images in parallel"
    if not format in IMAGE_FORMATS.keys():
        raise Exception("Image format is not supported")  # Wrong format
    img = load_s3image(file_base, format)
    
    queue   = Queue.Queue()
    # Populate hungry threads
    for item in db_imgs:
        tm  = ImageThread(queue, file_base, img, format)
        tm.setDaemon(True)
        tm.start()
    
    for item in db_imgs:
        queue.put(item)
        
    queue.join()


class ImageThread(threading.Thread):
    
    def __init__(self, queue, file_base, img, format):  # lock, 
        threading.Thread.__init__(self)
        self._queue     = queue
        self._file_base = file_base
        self._format    = format
        self._img       = img.copy()
    
    def run(self):
        (dim, dbimg)    = self._queue.get()
        proc_image(dim, dbimg, self._file_base, self._img, self._format)
        self._queue.task_done()


def crop_image(img, size):
    "Crops image"
    return img.crop((0, 0, size[0], size[1]))


def resize_image(img, size):
    "Resizes image"
    return img.resize(size)

# XXX: Specific for threads. Need a more general implementation
def proc_image(dim, dbimg, file_base, limg, format):
    "Processes image based on dimension and image size"
    # limg - loaded image
    img     = limg
    fmt     = IMAGE_FORMATS[format][1]    # "JPEG", "PNG"
    (iw, ih)    = img.size
    
    # For small image (dim > iw and dim > ih) no image processing is needed
    # Process image
    if dim > iw and dim < ih:       # tall image
        img = crop_image(img, (iw, dim))
    elif dim < iw and dim > ih:     # wide image
        img = crop_image(img, (dim, ih))
    elif dim < iw and dim < ih:     # large image
        if iw > ih:
            img = crop_image(img, (ih, ih))
        elif iw < ih:
            img = crop_image(img, (iw, iw))
        img = resize_image(img, (dim, dim))
        
    try:
        # Upload to S3
        fd      = StringIO.StringIO()
        img.save(fd, fmt)
        # Get file size
        fd.seek(0, 2)   # End of file
        size    = fd.tell()
            
        fd.seek(0)
        filename    = storage_filename(file_base, dbimg.size_type, format)
        
        (dbimg.width, dbimg.height)   = img.size
        dbimg.url      = storage.key2url(filename)
        dbimg.is_avail = storage.upload_file(fd, filename, IMAGE_FORMATS[format][0])
        dbimg.size     = size
        dbimg.format   = format
        dbimg.save()
    except Exception, e:
        logging.error("proc_image: %s %s" % (filename, str(e)))

    
