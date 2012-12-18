
from emapix.core.models import *

class WPhoto(object):
    
    @classmethod
    def request_photo(cls, res):
        "Returns request photo for the request"
        prs = PhotoRequest.objects.filter(request__resource=res).filter(photo__type="request")
        if not prs.exists():
            return None
        return prs[0].photo
    
    
    @classmethod
    def remove_photo(cls, res):
        pass
        #try:
        #
        
        
    @classmethod
    def remove_photo_throw(cls, res):
        pass