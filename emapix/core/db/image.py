from emapix.core.models import *

class WImage(object):
    
    @classmethod
    def get_or_create_image_by_request(cls, user, req, ph_type, filename):
        "Returns Image or creates Image object by request object"
        phreqs   = PhotoRequest.objects.filter(request=req).filter(photo__type=ph_type)
        
        if phreqs.exists():  # Use existing photo request
            ph      = phreqs[0].photo
        else:   # Create a new photo request
            ph      = Photo(user=user, type=ph_type, marked_delete=True)
            ph.save()
            phreq   = PhotoRequest(photo=ph, request=req)
            phreq.save()
        
        imgs    = Image.objects.filter(photo=ph)
        if imgs.exists():
            return imgs[0]
        return Image(photo=ph, name=filename)   # Create new Image


    @classmethod
    def get_image_by_resource(cls):
        pass

