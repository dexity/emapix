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

def url_crop_image(img_src, select_box):
    """
    url     - url of image
    select_box    - tuple of left upper corner coordinates, widht and height
    """
    (x, y, w, h)    = select_box
    
    # Download image from Amazon S3
    fd  = StringIO.StringIO()
    content_type    = s3_download_file(fd, img_src)
    fd.seek(0)
    im1     = Image.open(fd)
    im2     = im1.crop((x, y, x + w, y + h))
    fd.close()
    
    # Upload cropped image to Amazon S3
    fd      = StringIO.StringIO()
    im2.save(fd, im1.format)
    fd.seek(0)
    filename    = "cropped_pic." + IMAGE_TYPES[content_type]    # XXX: Might not be a valid content type
    s3_upload_file(fd, filename, content_type)     


class ImageThread(threading.Thread):
    
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    
    
    def run(self):
        proc_image(*self._queue.get())
        self._queue.task_done()


def proc_images():
    queue = Queue.Queue()
    params  = ((460, "pic_large.jpg"), (200, "pic_medium.jpg"), (50, "pic_small.jpg"))
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


def proc_image(dim, filename):
    "Processes image based on dimension and image size"
    # XXX: Load from S3
    
    img     = Image.open("/var/emapix/static/temp/cropped_pic.jpg")
    fmt     = img.format
    (iw, ih)    = img.size
    
    # dim > iw and dim > ih: # small image
    
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
        
    # XXX: Store in S3
    img.save("/var/emapix/static/temp/%s" % filename, fmt)     # save image
    
