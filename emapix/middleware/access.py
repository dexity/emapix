from emapix.views import forbidden, service_error

from emapix.settings import API_KEY     # Temp: get from db


class AccessMiddleware(object):
    
    def process_request(self, request):
        key = request.REQUEST.get("key", "")
        if key != API_KEY:
            return forbidden(request)
        # else just pass it on
        
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        method_name  = view_func.__name__
        
        from emapix.api.mappings import mappings
        # XXX: Import mappings according to the dispatched app
        if not method_name in mappings.keys():
            return service_error(request)
        
        # check required params
        req_params  = mappings[method_name]
        for param in req_params:
            if not param in request.REQUEST:
                return service_error(request) #mapping_error()