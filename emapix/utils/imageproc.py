import StringIO
from PIL import Image
import threading
import Queue

from emapix.utils import cloud_storage as storage
from emapix.utils.utils import storage_filename, timestamp
from emapix.utils.const import IMAGE_FORMATS
import logging


def crop_s3_image(img_name, crop_name, select_box):
    """
    img_name    - S3 key of the preview image
    crop_name   - S3 key of the crop image
    select_box  - tuple of left upper corner coordinates, widht and height

    Returns tuple (status, file_size)
    """
    (x, y, w, h) = select_box
    try:
        # Download selected image from Amazon S3
        fd = StringIO.StringIO()
        content_type = storage.download_file(fd, img_name)
        im1 = Image.open(fd)
        im2 = im1.crop((x, y, x + w, y + h))    # lazy operation
        fd.close()

        # Upload cropped image to Amazon S3
        fd = StringIO.StringIO()
        im2.save(fd, im1.format)
        # Get file size
        fd.seek(0, 2)   # End of file
        size = fd.tell()
        # Upload the image to Amazon S3
        fd.seek(0)  # Beginning of file
        status = storage.upload_file(fd, crop_name, content_type)
        return (status, size)
    except Exception, e:
        logging.error(str(e))
        return (False, 0)


def load_s3image(file_base, format):
    """Download cropped file from S3 and return Image object of the file."""
    filename = storage_filename(file_base, 'crop', format)
    fd = StringIO.StringIO()
    content_type = storage.download_file(fd, filename)
    return Image.open(fd)


def crop_image(img, size):
    """Crops image."""
    return img.crop((0, 0, size[0], size[1]))


def resize_image(img, size):
    """Resizes image."""
    return img.resize(size)


def dim4crop(dim, iw, ih, size_type=None):
    """Returns (width, height) dimensions tuple for crop."""
    if size_type == 'large':
        # No crop for large size type
        return

    # Process image for medium and small size types
    if (dim > iw) and (dim < ih):  # tall image
        return iw, dim
    if (dim < iw) and (dim > ih):  # wide image
        return dim, ih
    if (dim < iw) and (dim < ih):  # large image
        if iw > ih:
            return ih, ih
        if iw < ih:
            return iw, iw


def dim4resize(dim, iw, ih, size_type=None):
    """Returns (width, height) dimensions tuple for resize."""
    if size_type != 'large':  # Large image of medium and small size type
        if dim < iw and dim < ih:
            return dim, dim
        return

    nw = (iw * dim) / ih
    nh = (ih * dim) / iw

    # Process image for large. Keep proportion
    if (dim > iw) and (dim < ih):  # tall image
        return nw, dim
    if (dim < iw) and (dim > ih):  # wide image
        return dim, nh
    if (dim < iw) and (dim < ih):  # large image
        if iw > ih:
            return dim, nh
        elif iw < ih:
            return nw, dim


def proc_image(dim, dbimg, file_base, limg, format, size_type=None):
    """Processes image based on dimension and image size."""
    # limg - loaded image
    img = limg
    fmt = IMAGE_FORMATS[format][1]    # "JPEG", "PNG"
    (iw, ih) = img.size

    print dim, dbimg, file_base, limg, format, size_type

    # Crop image
    dims = dim4crop(dim, iw, ih, size_type)
    if dims is not None:
        img = crop_image(img, dims)

    # Resize image
    dims = dim4resize(dim, iw, ih, size_type)
    if dims is not None:
        img = resize_image(img, dims)

    try:
        # Upload to S3
        fd = StringIO.StringIO()
        img.save(fd, fmt)
        # Get file size
        fd.seek(0, 2)   # End of file
        size = fd.tell()

        fd.seek(0)
        filename = storage_filename(file_base, dbimg.size_type, format)
        upload_file_avail = storage.upload_file(
            fd, filename, IMAGE_FORMATS[format][0])

        (dbimg.width, dbimg.height) = img.size
        dbimg.is_avail = upload_file_avail
        dbimg.url = storage.key2url(filename)
        dbimg.size = size
        dbimg.format = format
        dbimg.save()
    except Exception, e:
        logging.error('proc_image: %s %s' % (filename, str(e)))


def image_serving_url(img):
    """Returns url from image object."""
    if not img:
        return ''
    return storage.key2url(img.name, 0, img.updated_time)


# Legacy way to process images in parallel
def proc_images(file_base, db_imgs, format):
    """Processes images in parallel."""
    if not format in IMAGE_FORMATS.keys():
        raise Exception('Image format is not supported')  # Wrong format
    img = load_s3image(file_base, format)

    queue = Queue.Queue()
    # Populate hungry threads
    for item in db_imgs:
        tm = ImageThread(queue, file_base, img, format)
        tm.setDaemon(True)
        tm.start()

    for item in db_imgs:
        queue.put(item)

    queue.join()


class ImageThread(threading.Thread):

    def __init__(self, queue, file_base, img, format):  # lock,
        threading.Thread.__init__(self)
        self._queue = queue
        self._file_base = file_base
        self._format = format
        self._img = img.copy()

    def run(self):
        (dim, dbimg) = self._queue.get()
        proc_image(dim, dbimg, self._file_base, self._img, self._format)
        self._queue.task_done()
