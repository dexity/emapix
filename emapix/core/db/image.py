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
        
        return cls.get_or_create_image_by_photo(ph, photo_type, size_type, marked_delete, save)


    @classmethod
    def get_image_by_request(cls, req, photo_type="request", size_type=None):
        "Returns Image object by request object"
        phreqs   = PhotoRequest.objects.filter(request=req).filter(photo__type=photo_type)
        if not phreqs.exists():
            return None
        
        return cls.get_image_by_photo(phreqs[0].photo, photo_type, size_type)


    @classmethod
    def get_or_create_profile_image(cls, user, photo_type, size_type=None, marked_delete=False, save=False):
        "Returns Image profile or creates Image profile object"
        profph   = ProfilePhoto.objects.filter(user=user).filter(photo__type=photo_type)
        
        if profph.exists():  # Use existing photo request
            ph      = profph[0].photo
        else:   # Create a new photo request
            ph      = Photo(user=user, type=photo_type, marked_delete=marked_delete)
            ph.save()
            phreq   = ProfilePhoto(photo=ph, user=user)
            phreq.save()
        
        return cls.get_or_create_image_by_photo(ph, photo_type, size_type, marked_delete, save)
    
    
    @classmethod
    def get_image_by_photo(cls, photo, photo_type, size_type=None):
        "Returns image by photo"
        imgs    = Image.objects.filter(photo=photo)
        if photo_type in ["request", "profile"]:
            imgs    = imgs.filter(size_type=size_type)
        if not imgs.exists():
            return None
        return imgs[0]
    
    
    @classmethod
    def get_or_create_image_by_photo(cls, photo, photo_type, size_type=None, marked_delete=False, save=False):
        "Returns or creates image by photo"
        img = cls.get_image_by_photo(photo, photo_type, size_type)
        if img:
            return img

        img = Image(photo=ph, size_type=size_type)
        if save:
            img.save()
        return img   # Create new Image        