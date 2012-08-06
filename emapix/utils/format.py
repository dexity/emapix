from django.http import HttpResponse
import json

def to_request(r):
    s   = {"id":    r.id,
           "lat":   r.lat,
           "lon":   r.lon,
           "submitted_date": r.submitted_date,
           "resource":  r.resource}
    return s

def to_json(obj):
    return json.dumps(obj)


def to_status(status, result=None):
    return HttpResponse(to_json({"status": status, "result": result}))