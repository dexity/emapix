import StringIO
from PIL import Image
import urllib2
import threading
import Queue
import time

from emapix.utils.amazon_s3 import s3_upload_file, s3_download_file
from emapix.core.db.image import WImage
from emapix.utils.utils import normalize_format, s3key

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
    #logger.debug(str(select_box))
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
        # Get file size
        fd.seek(0, 2)   # End of file
        size    = fd.tell()
        
        fd.seek(0)  # Beginning of file
        status  = s3_upload_file(fd, crop_name, content_type)
        return (status, size)
    except Exception, e:
        logger.debug(str(e))
        return (False, 0)


class ImageThread(threading.Thread):
    
    def __init__(self, queue, user, req, format):
        threading.Thread.__init__(self)
        self._queue     = queue
        self._user      = user
        self._request   = req
        self._format    = format
    
    def run(self):
        (dim, type) = self._queue.get()
        proc_image(dim, type, self._user, self._request, self._format)
        self._queue.task_done()


def proc_images(user, req, format):
    queue = Queue.Queue()
    params  = ((460, "large"), (200, "medium"), (50, "small"))
    for param in params:
        tm  = ImageThread(queue, user, req, format)
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


def proc_image(dim, type, user, req, format):
    "Processes image based on dimension and image size"
    res = req.resource
    # Download cropped file from S3
    filename    = s3key(res, "crop", format)
    fd  = StringIO.StringIO()
    content_type    = s3_download_file(fd, filename)
    
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
    # Get file size
    fd.seek(0, 2)   # End of file
    size    = fd.tell()
        
    fd.seek(0)
    filename    = s3key(res, type, format)
    
    # DB handling
    im  = WImage.get_or_create_image_by_request(user, req, type, filename)
    (im.width, im.height)   = img.size
    im.url      = s3_key2url(filename)
    im.is_avail = s3_upload_file(fd, filename, content_type)
    im.size     = size
    im.format   = format
    im.save()

    
