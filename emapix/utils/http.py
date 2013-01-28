import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError


def bad_form_json(form):
    "Returns json response for invalid form"
    errors  = form.errors.items()
    msg     = "Service error."
    if len(errors) == 0:
        return bad_request_json({"error": msg}) # Form is valid
    resp_errors = {}
    for e in errors:
        (name, value)   = (e[0], e[1][0])
        resp_errors[name]   = value
    return bad_request_json({"errors": resp_errors})    
    

def bad_request_json(obj):
    "Returns json response with 400 error status"
    return HttpResponseBadRequest(json.dumps(obj), mimetype="application/json")


def forbidden_json(obj):
    "Returns json response with 403 error status"
    return HttpResponseForbidden(json.dumps(obj), mimetype="application/json")

    
def http_response_json(obj):
    "Returns json response with 200 status"
    return HttpResponse(json.dumps(obj), mimetype="application/json")


def server_error_json(obj):
    "Returns json response with 500 error status"
    return HttpResponseServerError(json.dumps(obj), mimetype="application/json")