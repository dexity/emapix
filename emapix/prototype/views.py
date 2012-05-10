from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from emapix.utils import handle_uploaded_file
from forms import UploadFileForm

from emapix.utils.logger import Logger
logger = Logger.get("emapix.prototype.views")

def index(request):
    c = {}
    c.update(csrf(request))
    
    if request.method == 'POST':     
        form = UploadFileForm(request.POST, request.FILES)
        logger.debug(str(form))
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    c["form"]   = form
    return render_to_response('upload.html', c)

