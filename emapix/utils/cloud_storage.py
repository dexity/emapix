
from google.appengine.ext import blobstore
from google.appengine.api import images
from emapix.settings import BUCKET_NAME
import logging
import cloudstorage as gcs


def upload_file(fd, filename=None, content_type=None):
    if filename is None:
        filename = fd.name
    if content_type is None:
        content_type = fd.content_type

    try:
        filepath = file2path(filename)
        gcs_file = gcs.open(filepath, 'w', content_type=content_type)
        gcs_file.write(fd.read())
        gcs_file.close()
        fd.close()
        return True
    except Exception, e:
        logging.error('upload_file: %s %s' % (filename, str(e)))
    return False    # Not uploaded


def download_file(fd, filename):
    try:
        filepath = file2path(filename)
        gcs_file = gcs.open(filepath)
        stat = gcs.stat(filepath)
        fd.write(gcs_file.read())
        gcs_file.close()
        fd.seek(0)
        return stat.content_type
    except Exception, e:
        logging.error('download_file: %s %s' % (filename, str(e)))
    return None


def key2url(filename, max_serving_size=None, timestamp=None):
    """Returns url for the Cloud Storage."""
    blob_key = blobstore.create_gs_key('/gs' + file2path(filename))
    try:
        url = images.get_serving_url(blob_key)
        if url and max_serving_size is not None:
            url += '=s{}'.format(max_serving_size)
        if url and timestamp:
            url += '?t={}'.format(timestamp)  # Updates image cache
        return url
    except images.ObjectNotFoundError:
        pass
    return ''


def file2path(filename):
    """Returns file path in GCS."""
    return '/{}/{}'.format(BUCKET_NAME, filename)
