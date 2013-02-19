
from emapix.core.models import *

class WPhoto(object):
    
    @classmethod
    def get_profile_photo(cls, user, photo_type):
        "Returns profile photo object"
        profph   = ProfilePhoto.objects.filter(user=user)\
                        .filter(photo__type=photo_type)
        if photo_type not in ["preview", "crop"]:  # Used for creating profile image
            profph  = profph.exclude(photo__marked_delete=True)
        if not profph.exists():
            return None
        
        return profph[0]
    
    
    @classmethod
    def remove_profile_photo(cls, user):
        "Removes all records related to profile photos"
        profphotos = ProfilePhoto.objects.filter(user=user)
        profphs  = profphotos.filter(photo__type="profile")
        for pp in profphs:
            pp.photo.mark_delete()
        profphotos.delete()
        return True
        
    
    @classmethod
    def request_photo(cls, res):
        "Returns request photo for the request"
        prs = PhotoRequest.objects.filter(request__resource=res).filter(photo__type="request")
        if not prs.exists():
            return None
        return prs[0]
    
    
    @classmethod
    def photo_by_request(cls, res):
        rph = cls.request_photo(res)
        if not rph:
            return None
        return rph.photo
    
    
    @classmethod
    def remove_photo(cls, res):
        "Removes request photo"
        reqphotos  = PhotoRequest.objects.filter(request__resource=res)
        reqphs  = reqphotos.filter(photo__type="request")
        for rp in reqphs:
            rp.photo.mark_delete()
        reqphotos.delete()
        return True

   
