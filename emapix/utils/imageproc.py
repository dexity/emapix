import StringIO
from PIL import Image
import urllib2

IMAGE_TYPES = {
    "image/jpeg":   "jpg",
    "image/png":    "png"
}
from emapix.utils.logger import Logger
logger = Logger.get("emapix.utils.imageproc")

def crop_image(url, select_box):
    """
    url     - url of image
    select_box    - tuple of left upper corner coordinates, widht and height
    """
    (x, y, w, h)    = select_box
    resp    = urllib2.urlopen(url)
    headers = resp.info()
    type    = headers["Content-Type"]
    if type in IMAGE_TYPES:
        fd      = resp.read()   # Throws exception
        im1     = Image.open(StringIO.StringIO(fd))
        im2     = im1.crop((x, y, x + w, y + h))
        loc     = "/var/emapix/static/temp/cropped_pic." + IMAGE_TYPES[type]
        res     = im2.save(loc, im1.format)      
        
