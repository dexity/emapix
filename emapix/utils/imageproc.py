import StringIO
from PIL import Image
import urllib2
import threading
import Queue
import time
from emapix.utils.amazon_s3 import s3_upload_file, s3_download_file

IMAGE_TYPES = {
    "image/jpeg":   "jpg",
    "image/png":    "png"
}
from emapix.utils.logger import Logger
logger = Logger.get("emapix.utils.imageproc")

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
        content_type    = s3_download_file(fd, img_name)
        im1     = Image.open(fd)
        im2     = im1.crop((x, y, x + w, y + h))
        fd.close()
        
        # Upload cropped image to Amazon S3
        fd      = StringIO.StringIO()
        im2.save(fd, im1.format)
        fd.seek(0)
        status  = s3_upload_file(fd, crop_name, content_type)
        return (status, fd.size)
    except Exception, e:
        return (False, 0)


class ImageThread(threading.Thread):
    
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    
    
    def run(self):
        proc_image(*self._queue.get())
        self._queue.task_done()


def proc_images():
    queue = Queue.Queue()
    params  = ((460, "pic_large"), (200, "pic_medium"), (50, "pic_small"))
    for param in params:
        tm  = ImageThread(queue)
        tm.setDaemon(True)
        tm.start()
    
    for param in params:
        queue.put(param)
        
    queue.join()


def crop_image(img, size):
    "Crops image"
    return img.crop((0, 0, size[0], size[1]))


def resize_image(img, size):
    "Resizes image"
    return img.resize(size)


def proc_image(dim, fname_base):
    "Processes image based on dimension and image size"
    # Download from S3
    fd  = StringIO.StringIO()
    content_type    = s3_download_file(fd, "cropped_pic.jpg")
    
    img     = Image.open(fd)
    fmt     = img.format    # "JPEG", "PNG"
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
        
    # Upload to S3
    fd      = StringIO.StringIO()
    img.save(fd, fmt)
    fd.seek(0)
    filename    = "%s.%s" % (fname_base, IMAGE_TYPES[content_type])
    s3_upload_file(fd, filename, content_type)
    
