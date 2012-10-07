from emapix.core.models import *

class WImage(object):
    
    @classmethod
    def get_or_create_image_by_request(cls, user, req, photo_type, size_type=None, marked_delete=False, save=False):
        "Returns Image or creates Image object by request object"
        phreqs   = PhotoRequest.objects.filter(request=req).filter(photo__type=photo_type)
        
        if phreqs.exists():  # Use existing photo request
            ph      = phreqs[0].photo
        else:   # Create a new photo request
            ph      = Photo(user=user, type=photo_type, marked_delete=marked_delete)
            ph.save()
            phreq   = PhotoRequest(photo=ph, request=req)
            phreq.save()
        
        imgs    = Image.objects.filter(photo=ph)
        if photo_type == "request":
            imgs    = imgs.filter(size_type=size_type)
        if imgs.exists():
            return imgs[0]
        img = Image(photo=ph, size_type=size_type)
        if save:
            img.save()
        return img   # Create new Image


    @classmethod
    def get_image_by_request(cls, req, photo_type="request", size_type=None):
        "Returns Image object by request object"
        phreqs   = PhotoRequest.objects.filter(request=req).filter(photo__type=photo_type)
        if not phreqs.exists():
            return None
        
        imgs    = Image.objects.filter(photo=phreqs[0].photo)
        # Note: photo_size == None for photo_type in ["preview", "crop"]
        if photo_type == "request":
            imgs    = imgs.filter(size_type=size_type)
        if not imgs.exists():
            return None
        return imgs[0]
