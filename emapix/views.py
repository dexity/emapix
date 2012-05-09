from django.template import loader
from django.http import HttpResponseForbidden, HttpResponseServerError
    
def forbidden(request):
    # XXX: Should be json
    return HttpResponseForbidden(loader.render_to_string('403.html'),
                                 mimetype='text/html')
    
def service_error(request):
    # XXX: Should be json
    return HttpResponseServerError(loader.render_to_string('500.html'),
                                   mimetype='text/html')    