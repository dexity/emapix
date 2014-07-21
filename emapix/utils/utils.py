import hashlib
import time
import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.template.loaders.filesystem import Loader

from emapix.utils.const import *
import logging


def sha1(value):
    "Returns hex digest value of sha1 encryption"
    m   = hashlib.sha1()
    m.update(value)
    return m.hexdigest()


def random16():
    # Returns 16 characters string
    return sha1(str(time.time()))[:16]


def timestamp():
    return int(time.time())

def time_list(ts):
    "Converts timestamp to list: [day, hour, minute]"
    d   = ts / (60*60*24)
    h   = ts / (60*60) - d*24
    m   = ts / 60 - h*60 - d*24*60
    return [d, h, m]
    
    
def ts2hd(ts, show_year=True):
    "Converts timestamp to date string"
    df   = "%b %d, %H:%M"
    if show_year:
        df  = "%b %d, %Y %H:%M"
    return time.strftime(df, time.gmtime(int(ts)))


def show_year(ts0, ts1):
    "Returns true when years for ts0 and ts1 are different"
    y0  = time.gmtime(int(ts0)).tm_year
    y1  = time.gmtime(int(ts1)).tm_year
    return y0 != y1
    

def ts2h(ts0, ts1=None, full=True):
    "Converts timestamp to human readible string"
    if ts1 is None:
        return ts2hd(ts0)
    dt  = int(ts1) - int(ts0)
    if (dt < 0):    # Invalid time
        return ""
    sy  = show_year(ts0, ts1)
    if (dt > 432000):    # More than 5 days
        return ts2hd(ts0, sy)
    ht  = ""
    tl  = time_list(dt)
    # Compose string
    if tl[0] != 0:
        ht  = "%s d %s hr" % (tl[0], tl[1])
    elif tl[1] != 0:
        ht  = "%s hr %s min" % (tl[1], tl[2])
    elif tl[2] != 0:
        ht  = "%s min" % tl[2]
    else:
        ht  = "1 min"
    if full:
        ht  += " ago"
    return ht


def ts2utc(ts):
    "Gets timestamp and returns string in format: YYYY-MM-DD hh:mm:ssZ"
    try:
        utc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime(float(ts)))
    except Exception, e:    # Common exceptions: TypeError
        utc = ""
    return utc


def normalize_format(fmt):
    "Takes non-normalized format and returns normalized"
    if fmt in ["jpg", "png"]:
        return fmt
    if fmt in IMAGE_TYPES.keys():
        return IMAGE_TYPES[fmt]
    upper   = {"JPEG": "jpg", "JPG": "jpg", "PNG": "png"}
    if fmt in upper.keys():
        return upper[fmt]
    return None


def storage_filename(res, type, format):
    "Contructs S3 key from type and format"
    return "{}{}.{}".format(res, type, format)


def paginated_items(paginator, page_num):
    "Returns tuple of paginated items and page number"
    try:
        pn  = page_num
        if paginator.count > 0:
            if page_num == "last":
                pn  = paginator.num_pages
            elif page_num == "first":
                pn  = 1
        return (paginator.page(pn), int(pn))
    except PageNotAnInteger:
        return (paginator.page(1), 1)   # First page
    except EmptyPage:
        return (paginator.page(paginator.num_pages), paginator.num_pages)   # Out of range


def func2method(func,clas,method_name=None):
    """Adds func to class so it is an accessible method;
    use method_name to specify the name to be used for calling the method.
    The new method is accessible to any instance immediately."""
    func.im_class   = clas
    func.im_func    = func
    func.im_self    = None
    if not method_name:
        method_name = func.__name__
    clas.__dict__[method_name] = func
    

def is_you(request, user):
    "Checks if authenticated user is the same user"
    return request.user == user
    

def template_str(name):
    "Returns not rendered template string from template path"
    try:
        loader  = Loader()
        return loader.load_template_source(name)[0]
    except TemplateDoesNotExist:
        pass
    return ""
    
    
def change_number(cls, field_name, obj_sel, change_num):
    "Function for incrementing or decrementing fields (e.g. num_requests, num_photos ...)"
    if not obj_sel:
        return
    try:
        # obj_sel can be either dict (e.g. {user: self.user}) or an object
        if isinstance(obj_sel, dict):
            obj = cls.objects.get(**obj_sel)
        else:
            obj = obj_sel
        value   = getattr(obj, field_name) + change_num
        if value < 0:
            value = 0
        setattr(obj, field_name, value)
        obj.save()
    except Exception, e:
        logging.error("change_number failed: %s %s" % (cls.__name__, e))
    
    
def accept_json(request):
    "Returns True is Accept header is json"
    accept  = request.META["HTTP_ACCEPT"]
    if accept.startswith("application/json"):
        return True
    
    return False
    

def bad_form(form, mimetype="application/json"):
    "Returns response in mimetype for invalid form"
    errors  = form.errors.items()
    msg     = "Service error."
    if len(errors) == 0:
        return bad_request({"error": msg}, mimetype) # Form is valid
    resp_errors = {}
    for e in errors:
        (name, value)   = (e[0], e[1][0])
        resp_errors[name]   = value
    return bad_request({"errors": resp_errors}, mimetype)     
    
    
def bad_request(obj, mimetype="application/json"):
    "Returns response in mimetype with 400 error status"
    return HttpResponseBadRequest(json.dumps(obj), mimetype=mimetype)


def forbidden(obj, mimetype="application/json"):
    "Returns response in mimetype with 403 error status"
    return HttpResponseForbidden(json.dumps(obj), mimetype=mimetype)

    
def http_response(obj, mimetype="application/json"):
    "Returns response in mimetype with 200 status"
    return HttpResponse(json.dumps(obj), mimetype=mimetype)


def server_error(obj, mimetype="application/json"):
    "Returns response in mimetype with 500 error status"
    return HttpResponseServerError(json.dumps(obj), mimetype=mimetype)
    

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
  

