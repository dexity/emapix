
"""
Amazon S3 utils

Note:
    Need to specify parameters S3_KEY and S3_SECRET
"""

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf.settings import S3_KEY, S3_SECRET, BUCKET_NAME
import logging


def upload_file(fd, s3_filename=None, content_type=None):
    "Uploads file to S3 service from file descriptor"
    if s3_filename is None:
        s3_filename    = fd.name
    if content_type is None:
        content_type   = fd.content_type

    try:
        conn = S3Connection(S3_KEY, S3_SECRET)
        b   = conn.get_bucket(BUCKET_NAME)
        b.set_acl('public-read')
        
        k = Key(b)
        k.key = s3_filename
        k.set_metadata("Content-Type", content_type)
        k.set_contents_from_file(fd)    # Performs the actual upload
        k.set_acl('public-read')
        fd.close()
        return True
    except Exception, e:    # object doesn't exist or something else
        logging.error("upload_file: %s %s" % (s3_filename, str(e)))
    return False    # Not uploaded


def download_file(fd, s3_filename):
    "Sets content to file descriptor from S3 service"
    try:
        conn = S3Connection(S3_KEY, S3_SECRET)
        b   = conn.get_bucket(BUCKET_NAME)
        
        k   = Key(b)
        k.key   = s3_filename
        k.get_contents_to_file(fd)
        fd.seek(0)
        return k.content_type
    except Exception, e:
        logging.error("download_file: %s %s" % (s3_filename, str(e)))
    return None


def key2url(key):
    "Returns url for the Amazon S3 key"
    return "https://s3.amazonaws.com/%s/%s" % (BUCKET_NAME, key)
    
