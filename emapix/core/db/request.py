from emapix.core.models import *

class WRequest(object):
    
    @classmethod
    def remove_request(cls, res):
        "Removes request. Can through exception"
        req     = Request.objects.get(resource=res)
        req.location.delete()   # Remove location
        req.delete()
        return True    