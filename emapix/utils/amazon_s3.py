
"""
Amazon S3 utils
"""

from emapix.settings import S3_KEY, S3_SECRET, BUCKET_NAME

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from emapix.utils.logger import Logger
logger = Logger.get("emapix.utils.amazon_s3")


def s3_upload_file(fd, s3_filename=None, content_type=None):
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
        k.set_contents_from_file(fd) # Performs the actual upload
        k.set_acl('public-read')
        fd.close()
    except Exception, e:    # object doesn't exist or something else
        logger.debug(str(e))    


def s3_download_file(fd, s3_filename):
    "Sets content to file descriptor from S3 service"
    try:
        conn = S3Connection(S3_KEY, S3_SECRET)
        b   = conn.get_bucket(BUCKET_NAME)
        
        k   = Key(b)
        k.key   = s3_filename
        k.get_contents_to_file(fd)
        return k.content_type
    except Exception, e:
        logger.debug(str(e))
    return None


def resource2key(resource):
    return resource + ".jpg"


def file_exists(resource):
    # not used
    try:
        conn = S3Connection(S3_KEY, S3_SECRET)
        b   = conn.get_bucket(BUCKET_NAME)
        key = b.get_key(resource2key(resource))
        return key != None
    except Exception, e:
        logger.debug(str(e))
        return False


def handle_uploaded_file(file, resource):
    # Upload file to S3
    #open("/tmp/pic.jpg", "wb").write(file.read())    # works
    filename = str(file)
    if resource:
        filename    = "%s.jpg" % resource
    logger.debug(filename)
        
    try:
        conn = S3Connection(S3_KEY, S3_SECRET)
        b   = conn.get_bucket(BUCKET_NAME)
        b.set_acl('public-read')
        
        k = Key(b)
        k.key = filename
        k.set_metadata("Content-Type", 'image/jpeg')
        k.set_contents_from_file(file) # Performs the actual upload
        k.set_acl('public-read')
        
        # Record that file exists on S3
        _resource   = filename.split(".jpg")[0]
        prs  = PhotoRequest.objects.filter(resource=_resource)
        if (len(prs) > 0):
            pr  = prs[0]
            pr.photo_exists = True
            pr.save()
    except Exception, e:    # object doesn't exist or something else
        logger.debug(str(e))
        
        
        