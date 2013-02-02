
# Wrap classes for templates

from emapix.core.db.image import WImage
from emapix.utils.utils import *

class HumanTime(object):
    def __init__(self, ht, utc):
        self.human_time = ht
        self.utc_time   = utc
        

class RequestItem(object):
    request = None
    lat     = None
    lon     = None
    htime   = None
    thumb_url   = None
    

    
class TmplRequest(object):
    
    @classmethod
    def request_items(cls, requests):
        "Returns request items for request list template"
        ct  = timestamp()  # current time
        req_items  = []
        
        for req in requests:
            image   = WImage.get_image_by_request(req, size_type="small")
            thumb_url   = "/media/img/small.png"
            if image:
                thumb_url = image.url
            sd  = int(req.submitted_date)
            htime   = HumanTime(ts2h(sd, ct), ts2utc(sd))
            
            # Populate RequestItem
            ri  = RequestItem()
            ri.request  = req
            ri.lat  = req.location.lat/1e6
            ri.lon  = req.location.lon/1e6
            ri.htime    = htime
            ri.thumb_url    = thumb_url
            req_items.append(ri)
        return req_items