from emapix.core.models import *
from emapix.core.db.photo import WPhoto
from emapix.core.db.comment import WComment

class WRequest(object):
    
    @classmethod
    def get_recent_requests(cls):
        "Returns all recent requests"
        return Request.objects.all().order_by("-submitted_date")
        
        
    @classmethod
    def get_requests_by_location(cls):
        pass
        
        
    @classmethod
    def remove_request(cls, res):
        "Removes request. Can through an exception"
        # XXX: Request can only be removed by request owner
        req     = Request.objects.get(resource=res)
        req.location.delete()   # Remove location
        req.delete()
        return True
    
    
    @classmethod
    def purge_request_or_raise(cls, res, user):
        "Removes request and all related data"
        WPhoto.remove_photo_or_raise(res)
        WComment.remove_comments(res)
        cls.remove_request(res)

        