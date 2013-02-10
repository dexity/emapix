from emapix.core.models import *
from emapix.core.db.photo import WPhoto
from emapix.core.db.comment import WComment
from emapix.utils.utils import timestamp
from datetime import timedelta

class WRequest(object):
    
    @classmethod
    def get_recent_requests(cls, user=None, days=None, recent=True):
        "Returns recent requests filtered by user or days"
        reqs    = Request.objects.all()
        if user:
            reqs    = reqs.filter(user=user)
        if days:
            days_sec    = timedelta(days=days).total_seconds()
            days_ago  = timestamp() - days_sec      # days ago in seconds
            reqs    = Request.objects.filter(submitted_date__gt=days_ago)
        if recent:
            reqs    = reqs.order_by("-submitted_date")
        return reqs
        
        
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

        