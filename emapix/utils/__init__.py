
from emapix.settings import S3_KEY, S3_SECRET, BUCKET_NAME

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from emapix.api.models import PhotoRequest

from emapix.utils.logger import Logger
logger = Logger.get("utils.handle_uploaded_file")


# S3 related utils

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


def list_files():
    pass


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


    
    
    