from django.http import HttpResponse
import json

# XXX: Refactor this module
def to_request(r):
    s   = {"id":    r.id,
           "lat":   "",
           "lon":   "",
           "description": r.description,
           "submitted_date": r.submitted_date,
           "resource":  r.resource}
    if r.location:
        s["lat"]    = r.location.lat
        s["lon"]    = r.location.lon
    return s


def to_requests(rs):
    l   = []
    for r in rs:
        l.append(to_request(r))
    return l


def to_json(obj):
    return json.dumps(obj)


def to_status(status, result=None):
    return HttpResponse(to_json({"status": status, "result": result}))