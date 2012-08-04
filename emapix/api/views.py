import json
import time

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from emapix.utils import handle_uploaded_file, file_exists
from emapix.utils.utils import timestamp
from emapix.utils.format import *
from emapix.utils.const import OK, FAIL

from emapix.api.models import PhotoRequest 


from emapix.utils.logger import Logger
logger = Logger.get("emapix.api.views")

def add(request):
    "Adds record to the photo request"
    p   = request.REQUEST
    try:
        pr  = PhotoRequest(lat=p["lat"], lon=p["lon"], submitted_date=timestamp(), 
                           resource=p["resource"])
        pr.save()
        return to_status(OK, to_photo(pr))
    except Exception, e:
        logger.debug(str(e))
        return to_status(FAIL, str(e))


def remove(request, reqid):
    "Removes record from the photo request"
    try:
        pr  = PhotoRequest.objects.get(id=reqid)
        pr.delete()
        return to_status(OK)
    except Exception, e:
        logger.debug(str(e))
        return to_status(FAIL, str(e))


def _update_photo_request(pr):
    "Checks if file actually exists and updates"
    # not used
    if file_exists(pr.resource):
        pr.photo_exists = True
        pr.save()
    
    
def _update_list_photo_request(prs):
    "Checks S3 data set with "
    # not used
    pass


# cache file check
def get(request, reqid):
    try:
        pr  = PhotoRequest.objects.get(id=reqid)
        #_update_photo_request(pr)   # hide
        return to_status(OK, to_photo(pr))
    except Exception, e:
        logger.debug(str(e))
        return to_status(FAIL, str(e))


# cache file check
def get_all(request):
    try:
        prs  = PhotoRequest.objects.all()
        #_update_list_photo_request(prs)
        l   = []
        for p in prs:
            l.append(to_photo(p))
        return to_status(OK, l)
    except Exception, e:
        logger.debug(str(e))
        return to_status(FAIL)


def update(request, reqid):
    p   = request.REQUEST
    try:
        pr  = PhotoRequest.objects.get(id=reqid)
        pr.resource = p["resource"]
        pr.save()
        return to_status(OK, to_photo(pr))
    except Exception, e:
        logger.debug(str(e))
        return to_status(FAIL, str(e))


def upload(request):
    "Uploads file to S3"  
    logger.debug(request.FILES.keys())
    if request.method == 'POST':
        # XXX: Check status of uploaded file
        handle_uploaded_file(request.FILES['uploaded'], request.REQUEST.get("resource", None))
        return to_status(OK)
        #return HttpResponseRedirect('/')           
    
    # XXX: Change default response
    return to_status(OK)
    


