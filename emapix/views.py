from django.template import loader
from django.http import HttpResponseForbidden
    
def forbidden(request):
    return HttpResponseForbidden(loader.render_to_string('403.html'),
                                 mimetype='text/html')