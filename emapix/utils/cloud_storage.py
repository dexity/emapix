
from emapix.settings import BUCKET_NAME
import logging
import cloudstorage as gcs

def upload_file(fd, filename=None, content_type=None):
    if filename is None:
        filename    = fd.name
    if content_type is None:
        content_type   = fd.content_type

    try:
        gcs_file = gcs.open(filename, 'w', content_type=content_type)
        gcs_file.write(fd.read())
        gcs_file.close()
        return True
    except Exception, e:
        logging.error("upload_file: %s %s" % (filename, str(e)))
    return False    # Not uploaded


def download_file(fd, filename):
    try:
        gcs_file = gcs.open(filename)
        stat = gcs.stat(filename)
        fd.write(gcs_file.read())
        fd.seek(0)
        gcs_file.close()
        fd.close()
        return stat.content_type
    except Exception, e:
        logging.error("download_file: %s %s" % (filename, str(e)))
    return None


def key2url(key):
    "Returns url for the Cloud Storage"
    return 'https://storage.googleapis.com/{}/{}'.format(BUCKET_NAME, key)
