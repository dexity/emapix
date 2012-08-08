from django.http import HttpResponse
import json

def to_request(r):
    s   = {"id":    r.id,
           "lat":   r.lat,
           "lon":   r.lon,
           "description": r.description,
           "submitted_date": r.submitted_date,
           "resource":  r.resource}
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