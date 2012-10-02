from emapix.core.models import *

class WImage(object):
    
    @classmethod
    def get_or_create_image_by_request(cls, user, req, photo_type, filename, marked_delete=False):
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
        if imgs.exists():
            return imgs[0]
        img = Image(photo=ph, name=filename)
        img.save()
        return img   # Create new Image


    @classmethod
    def get_image_by_request(cls, req, photo_size, photo_type="request"):
        "Returns Image object by request object"
        # XXX: Finish filtering by size. See Q() filter
        phreqs   = PhotoRequest.objects.filter(request=req).filter(photo__type=photo_type)
        if not phreqs.exists():
            return None
        
        imgs    = Image.objects.filter(photo=phreqs[0].photo)
        if not imgs.exists():
            return None
        return imgs[0]
