from emapix.utils.utils import http_response_json
import json

# XXX: Refactor this module


def to_request(r):
    """Serializes request."""
    if not r:
        return {}
    s = {
        'id':    r.id,
        'lat':   '',
        'lon':   '',
        'description': r.description,
        'submitted_date': r.submitted_date,
        'resource':  r.resource
    }
    if r.location:
        s['lat'] = r.location.lat
        s['lon'] = r.location.lon
    return s


def to_requests(rs):
    l = []
    for r in rs:
        l.append(to_request(r))
    return l


def to_ok():
    return http_response_json({'status': 'ok'})


def to_json(obj):
    return json.dumps(obj)


# Remove?
def to_status(status, result=None):
    """Returns s."""
    resp = {
        'status': status
    }
    if result is not None:
        resp['result'] = result
    return http_response_json(resp)
