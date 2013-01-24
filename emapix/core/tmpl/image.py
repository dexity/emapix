
from emapix.core.db.image import WImage

# Not tested
class Image(object):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TmplImage(object):
    
    @classmethod
    def photo_request_images(cls, phreqs, size_type="medium"):
        images  = []
        for phreq in paged_phreqs:
            image   = WImage.get_image_by_photo(phreq.photo, size_type=size_type)
            kwargs  = {
                "resource":     phreq.request.resource,
                "description":  phreq.request.description,
                "image_url":    image.url   # XXX: image can be None
            }
            images.append(Image(**kwargs))
        return images