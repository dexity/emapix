from django.http import HttpResponse
import json

def to_photo(p):
    s   = {"id":    p.id,
           "lat":   p.lat,
           "lon":   p.lon,
           "submitted_date": p.submitted_date,
           "resource":  p.resource,
           "photo_exists":  p.photo_exists}
    return s

def to_json(obj):
    return json.dumps(obj)


def to_status(status, result=None):
    return HttpResponse(to_json({"status": status, "result": result}))