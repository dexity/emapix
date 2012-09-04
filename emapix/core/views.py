import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django.contrib.auth as django_auth

from emapix.utils.const import *
from emapix.utils.utils import sha1, random16, timestamp, ts2h, ts2utc, ts2hd, handle_uploaded_file
from emapix.utils.format import *
from emapix.core.forms import *
from emapix.core.models import *
from emapix.core.dbutils import db_remove_request
from emapix.utils.google_geocoding import latlon2addr
from emapix.core.emails import send_activation_email, send_forgot_email, send_newpass_confirm_email

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.views")

def index(request):
    return render_to_response("index.html")


def generate_token(value):
    "Generates 40 character token"
    return sha1(value + str(time.time()))
    

class HumanTime(object):
    def __init__(self, ht, utc):
        self.human_time = ht
        self.utc_time   = utc
        

@csrf_protect
def join(request):
    
    if request.method == "POST":
        form    = JoinForm(request.POST)
        if form.is_valid():
            username    = form.cleaned_data["username"]
            email       = form.cleaned_data["email"]
            password    = form.cleaned_data["password"]
            
            # Creates user
            try:
                user        = User(username=username, email=email)    #.objects.create_user(username, email, password)
                user.set_password(password)
                user.is_active  = False
                user.save()
            except:
                c   = {
                    "form":     form
                }
                return render(request, "join.html", c)                

            profile     = UserProfile()
            profile.user    = user
            
            profile.location    = form.cleaned_data["location"]
            profile.country     = form.cleaned_data["country"]
            b_day   = form.cleaned_data["b_day"]
            if b_day:
                profile.b_day   = b_day
            profile.b_month     = form.cleaned_data["b_month"]
            profile.b_year      = form.cleaned_data["b_year"]
            profile.gender      = form.cleaned_data["gender"]
            
            token   = generate_token(username)  # token for confirmation
            profile.activ_token = token
            profile.save()
            
            send_activation_email(request, email, username, token)

            # TODO: Add reCAPTCHA verification
            #return HttpResponseRedirect("/verify")
            return render(request, "message.html", {"type": "verify"})
    else:
        form    = JoinForm()

    c   = {
        "form":     form
    }
    return render(request, "join.html", c)


def verify(request):
    # TODO: Add reCAPTCHA verification
    #return render(request, "message.html", {"type": "verify"})
    pass


def confirm(request, token):
    # Check user token
    c   = {}
    try:
        profile = UserProfile.objects.get(activ_token = token)
        profile.user.is_active  = True
        profile.user.save()
        profile.activ_token = None
        profile.save()
        c   = {"type": "confirm"}
    except Exception, e:
        logger.debug(str(e))
        c   = {"type": "confirm_failed"}

    return render(request, "message.html", c)


@csrf_protect
def login(request):
    if request.method == "POST":
        form    = LoginForm(request.POST)
        if form.is_valid():
            django_auth.login(request, form.cleaned_data["user"])   # should have user authenticated already
            return HttpResponseRedirect("/")
    else:
        form    = LoginForm()
    c   = {
        "form": form
    }
    return render(request, 'login.html', c)


def logout(request):
    django_auth.logout(request)
    return HttpResponseRedirect("/")


@csrf_protect
def forgot(request):
    if request.method == "POST":
        form    = ForgotForm(request.POST)
        if form.is_valid():
            user    = form.cleaned_data["user"]
            try:
                profile = UserProfile.objects.get(user=user)
            
                token   = generate_token(user.username)
                profile.forgot_token    = token
                profile.save()
                
                send_forgot_email(request, user.email, user.username, token)
                return render(request, "message.html", {"type": "forgot"})
            
            except Exception, e:
                logger.debug(str(e))
    else:
        form    = ForgotForm()
    c   = {
        "form": form
    }
    return render(request, 'forgot.html', c)


@csrf_protect
def renew_password(request, token):

    try:
        profile = UserProfile.objects.get(forgot_token = token)
        if request.method == "POST":
            form    = NewPasswordForm(request.POST)
            if form.is_valid():
                newpass = form.cleaned_data["newpass"]
                profile.forgot_token = ""
                profile.user.set_password(newpass)
                profile.user.save() # Important
                profile.save()
                
                email   = profile.user.email
                username    = profile.user.username
                # Send email
                send_newpass_confirm_email(request, email, username)
                return render(request, "message.html", {"type": "newpass_success"})
        else:
            form    = NewPasswordForm()
        c   = {
            "form":     form,
            "token":    token
        }
        return render(request, "newpass.html", c)
        
    except Exception, e:
        logger.debug(str(e))
        return render(request, "message.html", {"type": "newpass_failed"})


def make_request(request):
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}
    return render_to_response('make.html', c)


@csrf_protect
def add_request(request):
    "Displays and handles photo request form"
    if not request.user.is_authenticated():
        return render_to_response('forms/request_form.html')
    
    _user   = request.user
    c   = {
        "username": _user
    }
        
    if request.method == "POST":
        # POST request
        form    = RequestForm(request.POST)
        if form.is_valid():
            p   = request.POST
            lat = form.cleaned_data["lat"]
            lon = form.cleaned_data["lon"]
            
            # Create Location
            l   = Location()
            l.lat   = 1e6*lat
            l.lon   = 1e6*lon
            
            # Set address (to separate function)
            addr    = latlon2addr(lat, lon)
            if addr is not None:
                ll  = addr[0]
                l.res_lat   = ll[0]
                l.res_lon   = ll[1]
                (l.street, l.city, l.country) = addr[1]
                l.res_type  = addr[2]
                l.zipcode   = addr[3]
                
            l.save()
            
            # Create Request
            r   = Request()
            r.user  = _user
            r.location  = l
            r.description   = form.cleaned_data["description"]
            r.submitted_date    = timestamp()
            r.resource  = random16()
            r.save()
            
            return to_status(OK, to_request(r))
        else:
            lat     = request.POST.get("lat", "")
            lon     = request.POST.get("lon", "")
    else:
        # GET request
        lat = request.GET.get("lat", "")
        lon = request.GET.get("lon", "")
        form    = RequestForm(initial={"lat": lat, "lon": lon})
    
    c["lat"]    = lat
    c["lon"]    = lon        

    # Check is request limit is reached
    reqs    = Request.objects.filter(user=_user)
    ups     = UserProfile.objects.filter(user=_user)
    if (len(ups) > 0 and len(reqs) >= ups[0].req_limit):
        c["limit_reached"]  = True
        c["max_limit"]  = ups[0].req_limit
    
    c["form"]   = form
    
    return render(request, 'forms/request_form.html', c)


def get_requests_json(request):
    # Returns list of all user's markers
    if not request.user.is_authenticated():
        return to_status(FAIL, "User is not authenticated")
    
    _user   = request.user
    reqs    = Request.objects.filter(user=_user)
    return to_status(OK, to_requests(reqs))


def request_info(request, res):
    "Displays the request info"
    if not request.user.is_authenticated():
        return render(request, 'ajax/request_info.html')
    
    c   = {"username": request.user}    
    reqs = Request.objects.filter(resource=res)
    if len(reqs) > 0:
        req = reqs[0]
        c["req_exists"]  = True
        c["id"]     = req.id
        if req.location:
            c["lat"]    = req.location.lat/1e6
            c["lon"]    = req.location.lon/1e6
            c["street"] = req.location.street
            c["city"]   = req.location.city
            c["country"]    = req.location.country
        c["description"]    = req.description
        c["resource"]   = req.resource

    return render(request, 'ajax/request_info.html', c)


def get_request(request, res):
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}
    try:
        req = Request.objects.get(resource=res)
        req.location.lat    = req.location.lat/1e6
        req.location.lon    = req.location.lon/1e6
        c["req"]    = req
        c["hdate"]  = ts2hd(req.submitted_date)
        c["utcdate"]    = ts2utc(req.submitted_date)
    except Exception, e:
        pass
    return render(request, 'request.html', c)


def remove_request(request, res):
    "Removes request"
    if not request.user.is_authenticated():
        return render(request, 'ajax/error.html', {"error": AUTH_ERROR})
    
    if request.method != "POST":
        return render(request, 'ajax/error.html', {"error":  "Invalid request" })
    try:
        db_remove_request(res)
        return to_status(OK)
    except Exception, e:
        return render(request, 'ajax/error.html', {"error":  "Request does not exist"})



def set_profile(request):
    return render_to_response('set_profile.html')

def set_password(request):
    return render_to_response('set_password.html')

def get_user(request, username):
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}
    try:
        user    = User.objects.get(username)
        c["user"]   = user
    except:
        pass
    return render(request, 'profile.html', c)


def users(request):
    return render_to_response('users.html')

def help(request):
    return render_to_response('help.html')


def get_requests(request):
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}
    reqs    = Request.objects.all().order_by("-submitted_date")
    paginator   = Paginator(reqs, 30)   # 30 items per page
    page    = request.GET.get("page")
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)    
    
    ct  = int(time.time())  # current time
    ht  = []
    for item in items:
        sd  = int(item.submitted_date)
        t   = HumanTime(ts2h(sd, ct), ts2utc(sd))
        ht.append(t)
        item.location.lat   = item.location.lat/1e6
        item.location.lon   = item.location.lon/1e6
    
    c["items"]  = zip(items, ht)
    c["paginator"]  = paginator
    return render(request, 'requests.html', c)


def request2(request):
    return render_to_response('request2.html')

def photos(request):
    return render_to_response('photos.html')

def search(request):
    return render_to_response('search.html')

def search2(request):
    return render_to_response('search2.html')

def submit(request, res):
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}
    try:
        req = Request.objects.get(resource=res)
        c["req"]    = req
    except Exception, e:
        pass
    return render(request, 'submit.html', c)

TEMP_UP = """{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td class="preview"><span class="fade"></span></td>
        <td class="name"><span>{%=file.name%}</span></td>
        <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
        {% if (file.error) { %}
            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else if (o.files.valid && !i) { %}
            <td>
                <div class="progress progress-success progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="bar" style="width:0%;"></div></div>
            </td>
            <td class="start">{% if (!o.options.autoUpload) { %}
                <button class="btn btn-primary">
                    <i class="icon-upload icon-white"></i>
                    <span>{%=locale.fileupload.start%}</span>
                </button>
            {% } %}</td>
        {% } else { %}
            <td colspan="2"></td>
        {% } %}
        <td class="cancel">{% if (!i) { %}
            <button class="btn btn-warning">
                <i class="icon-ban-circle icon-white"></i>
                <span>{%=locale.fileupload.cancel%}</span>
            </button>
        {% } %}</td>
    </tr>
{% } %}"""

TEMP_UP2 = """{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td class="preview"><span class="fade"></span></td>
        <td class="name"><span>{%=file.name%}</span></td>
        <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
        {% if (file.error) { %}
            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else if (o.files.valid && !i) { %}
            <td>
                <div class="progress progress-success progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="bar" style="width:0%;"></div></div>
            </td>
            <td class="start">{% if (!o.options.autoUpload) { %}
                <button class="btn btn-primary">
                    <i class="icon-upload icon-white"></i>
                    <span>{%=locale.fileupload.start%}</span>
                </button>
            {% } %}</td>
        {% } else { %}
            <td colspan="2"></td>
        {% } %}
        <td class="cancel">{% if (!i) { %}
            <button class="btn btn-warning">
                <i class="icon-ban-circle icon-white"></i>
                <span>{%=locale.fileupload.cancel%}</span>
            </button>
        {% } %}</td>
    </tr>
{% } %}"""

TEMP_DN = """{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-download fade">
        {% if (file.error) { %}
            <td></td>
            <td class="name"><span>{%=file.name%}</span></td>
            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else { %}
            <td class="preview">{% if (file.thumbnail_url) { %}
                <a href="{%=file.url%}" title="{%=file.name%}" rel="gallery" download="{%=file.name%}"><img src="{%=file.thumbnail_url%}"></a>
            {% } %}</td>
            <td class="name">
                <a href="{%=file.url%}" title="{%=file.name%}" rel="{%=file.thumbnail_url&&'gallery'%}" download="{%=file.name%}">{%=file.name%}</a>
            </td>
            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
            <td colspan="2"></td>
        {% } %}
        <td class="delete">
            <button class="btn btn-danger" data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}">
                <i class="icon-trash icon-white"></i>
                <span>{%=locale.fileupload.destroy%}</span>
            </button>
            <input type="checkbox" name="delete" value="1">
        </td>
    </tr>
{% } %}"""

def submit2(request):
    # Testing file uploading
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}
        
    if request.method == "POST":
        fd  = request.FILES["files[]"]
        try:
            # XXX: Fix file saving
            # XXX: Check if file resizing occures!
            open("/tmp/pic.png", "wb").write(fd);   
        except Exception, e:
            logger.debug(str(e))
        return HttpResponse(json.dumps({"status": "ok"}), mimetype="application/json")
    
        #x   = request.POST.get("x", None)
        #y   = request.POST.get("y", None)
        #h   = request.POST.get("h", None)
        #w   = request.POST.get("w", None)
        #if x and y and h and w:
        #    logger.debug("x=%s; y=%s; h=%s, w=%s" % (x, y, h, w))
        #form   = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        #    fd  = request.FILES['file']
        #    if not fd.content_type in IMAGE_CONTENT_TYPES:  # Not supported types
        #        # Return error
        #        pass
        #    handle_uploaded_file(fd)
        
        # XXX: Set to S3 url for preview image
        #c["preview_url"]    = ""
        
        # XXX: Keep selection if something went wrong
        crop_form   = CropForm()
        c["crop_form"]  = crop_form        
        return HttpResponseRedirect("/submit2")
    else:
        form   = UploadFileForm()
        
    c["form"]       = form
    c["temp_up"]    = TEMP_UP2
    c["temp_dn"]    = TEMP_DN
    return render(request, 'submit2.html', c)


def submit3(request):
    return render_to_response('submit3.html')



