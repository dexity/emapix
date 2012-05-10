
from emapix.settings import S3_KEY, S3_SECRET, BUCKET_NAME

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from emapix.utils.logger import Logger
logger = Logger.get("utils.handle_uploaded_file")

def handle_uploaded_file(file):
    # Upload file to S3
    #open("/tmp/pic.jpg", "wb").write(file.read())    # works
    filename = str(file)
    try:
        conn = S3Connection(S3_KEY, S3_SECRET)
        rs  = conn.get_all_buckets()
        b   = rs[0]
        b.set_acl('public-read')
        
        k = Key(b)
        k.key = filename
        k.set_metadata("Content-Type", 'image/jpeg')
        k.set_contents_from_file(file) # Performs the actual upload
        k.set_acl('public-read')
    except Exception, e:
        logger.debug(str(e))

    
    
    