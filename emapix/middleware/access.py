from django.http import HttpResponse
from emapix.settings import API_KEY

class AccessMiddleware(object):
    
    def process_request(self, request):
        return HttpResponse("Hello")