from emapix.core.models import *

class WRequest(object):
    
    @classmethod
    def remove_request(cls, res):
        "Removes request. Can through an exception"
        # XXX: Request can only be removed by request owner
        req     = Request.objects.get(resource=res)
        req.location.delete()   # Remove location
        req.delete()
        return True
    
    @classmethod
    def purge_request(cls, res, user):
        "Removes request and all related data"
        cls.remove_request(res)
        # Remove PhotoRequest
        
        # Remove Photo
        
        # Remove Image(s)
        
        # Remove files from S3 service
        
        # Remove RequestComment(s) (in the future)
        
        # Remove Comment(s) (in the future)

        