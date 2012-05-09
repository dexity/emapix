from django.http import HttpResponse
from models import PhotoRequest
import json
import time

OK      = "ok"
FAIL    = "fail"


def add(request):
    "Adds record to the photo request"
    p   = request.REQUEST
    try:
        pr  = PhotoRequest(lat=p["lat"], lon=p["lon"], submitted_date=timestamp(), resource=p["resource"])
        pr.save()
        return to_status(OK, to_photo(pr))
    except:
        return to_status(FAIL)


def remove(request, reqid):
    "Removes record from the photo request"
    try:
        pr  = PhotoRequest.objects.get(id=reqid)
        pr.delete()
        return to_status(OK)
    except:
        return to_status(FAIL)


def get(request, reqid):
    try:
        pr  = PhotoRequest.objects.get(id=reqid)
        return to_status(OK, to_photo(pr))
    except:
        return to_status(FAIL)


def get_all(request):
    try:
        prs  = PhotoRequest.objects.all()
        l   = []
        for p in prs:
            l.append(to_photo(p))
        return to_status(OK, l)
    except:
        return to_status(FAIL)



def update(request, reqid):
    p   = request.REQUEST
    try:
        pr  = PhotoRequest.objects.get(id=reqid)
        pr.resource = p["resource"]
        pr.save()
        return to_status(OK, to_photo(pr))
    except:
        return to_status(FAIL)


# Move to some other class

def timestamp():
    return int(time.time())

def to_photo(p):
    s   = {"id":    p.id,
           "lat":   p.lat,
           "lon":   p.lon,
           "submitted_date": p.submitted_date,
           "resource":  p.resource}
    return s

def to_json(obj):
    return json.dumps(obj)


def to_status(status, result=None):
    return HttpResponse(to_json({"status": status, "result": result}))
