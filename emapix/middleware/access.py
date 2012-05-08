from emapix.views import forbidden
from emapix.settings import API_KEY # Temp

class AccessMiddleware(object):
    
    def process_request(self, request):
        key = request.REQUEST.get("key", "")
        if key != API_KEY:
            return forbidden(request)
        # else just pass it on