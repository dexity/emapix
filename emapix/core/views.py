
# -*- coding: utf-8 -*-

import time

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest  # remove
from django.shortcuts import render_to_response, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django.contrib.auth as django_auth
from django.core.files.images import ImageFile
from django.conf import settings

from emapix.utils.const import *
from emapix.utils.utils import sha1, random16, timestamp, ts2h, ts2utc, ts2hd, bad_request_json, \
http_response_json, forbidden_json, s3key, paginated_items, is_you, bad_form_json
from emapix.core.validators import validate_user_request
from emapix.utils.format import *
from emapix.utils.imageproc import crop_s3_image, proc_images
from emapix.core.forms import *
from emapix.core.models import *
from emapix.utils.google_geocoding import latlon2addr
from emapix.core.emails import send_activation_email, send_forgot_email, send_newpass_confirm_email
from emapix.utils.amazon_s3 import s3_upload_file, s3_key2url
from emapix.core.db.image import WImage
from emapix.core.db.request import WRequest
from emapix.core.db.comment import WComment
from emapix.core.tmpl.request import TmplRequest
from emapix.core.forms import RecaptchaForm

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.views")

#def index(request):
#    return render_to_response("index.html")


def generate_token(value):
    "Generates 40 character token"
    return sha1(value + str(time.time()))
    

@csrf_protect
def join(request):
    "Submits registration form and sends activation email"
    clean_join_session(request)
    
    if request.method == "POST":
        form    = JoinForm(request.POST)
        if form.is_valid():
            request.session.set_expiry(3600)    # 1 hour
            join_session    = {
                "username":     form.cleaned_data["username"],
                "email":        form.cleaned_data["email"],
                "password":     form.cleaned_data["password"],
                "location":     form.cleaned_data["location"],
                "country":      form.cleaned_data["country"],
                "b_day":        form.cleaned_data["b_day"],
                "b_month":      form.cleaned_data["b_month"],
                "b_year":       form.cleaned_data["b_year"],
                "gender":       form.cleaned_data["gender"],
                "token":        generate_token(form.cleaned_data["username"])  # token for confirmation    
            }

            request.session["join"] = join_session
            return HttpResponseRedirect("/recaptcha")
    else:
        form    = JoinForm()

    c   = {
        "form":     form,
        "hide_join":    True
    }
    return render(request, "join.html", c)


@csrf_protect
def handle_recaptcha(request):
    "Handles recaptcha"
    # Recaptcha is only available if it is redirected from join form
    if not "join" in request.session:
        return render(request, "misc/error_view.html", {"error": "Long time no see. Please try again"})
    
    form    = RecaptchaForm()
    
    if request.method == "POST":
        form    = RecaptchaForm(request.POST)
        if form.is_valid():
            
            join_session    = request.session["join"]
            username        = join_session["username"]
            email           = join_session["email"]
            token           = join_session["token"]
            
            join_form       = JoinForm()    # XXX: Bind the form
            # Creates user
            try:
                user        = User()
                user.username = username
                user.email  = email
                user.set_password(join_session["password"])
                user.is_active  = False
                user.save()
            except Exception, e:
                logger.error(str(e))
                c   = {
                    "form":     join_form,
                    "hide_join":    True
                }
                return render(request, "join.html", c)
            
            profile     = UserProfile()
            profile.user    = user
            
            profile.location    = join_session["location"]
            profile.country     = join_session["country"]
            b_day   = join_session["b_day"]
            if b_day:
                profile.b_day   = b_day
            profile.b_month     = join_session["b_month"]
            profile.b_year      = join_session["b_year"]
            profile.gender      = join_session["gender"]
            
            profile.activ_token = token
            profile.save()
            
            send_activation_email(request, email, username, token)
            
            clean_join_session(request)
            request.session.set_expiry(None)
            
            return render(request, "message.html", {"type": "verify", "hide_join": True})
    
    c   = {
        "form":  form,
        "hide_join":    True
    }
    return render(request, "recaptcha.html", c)


def clean_join_session(request):
    "Remove join session"
    try:
        del request.session["join"]
    except KeyError:
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
        c   = {
            "type": "confirm",
            "hide_join":    True
        }
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
        "form": form,
        "hide_join":    True
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
                logger.error(str(e))
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
    c   = {}
    return render(request, 'make.html')


@csrf_protect
def add_request(request):
    "Displays and handles photo request form"
    if not request.user.is_authenticated():
        logger.debug(str(request.user))
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    
    _user   = request.user
    c   = {}
        
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
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    
    try:
        req = Request.objects.get(resource=res)
        c   = {}
        c["id"]     = req.id
        if req.location:
            c["lat"]    = req.location.lat/1e6
            c["lon"]    = req.location.lon/1e6
            c["street"] = req.location.street
            c["city"]   = req.location.city
            c["country"]    = req.location.country
        c["description"]    = req.description
        c["resource"]   = req.resource
    except Request.DoesNotExist:
        return render(request, 'misc/error_view.html', {"error": "Request does not exist"})
    
    return render(request, 'ajax/request_info.html', c)


def get_request(request, res):
    "Returns request"
    try:
        req = Request.objects.get(resource=res)
        req.location.lat    = req.location.lat/1e6
        req.location.lon    = req.location.lon/1e6
        img = WImage.get_image_by_request(req, size_type="large")
        
        c   = {
            "req":      req,
            "is_you":   is_you(request, req.user),
            "hdate":    ts2hd(req.submitted_date),
            "utcdate":  ts2utc(req.submitted_date),
        }

        if isinstance(img, Image):
            c["pic_url"]    = img.url
    except Request.DoesNotExist:
        return render(request, "misc/error_view.html", {"error": "Request does not exist"})
    
    return render(request, 'request.html', c)


@csrf_protect
def edit_request_ajax(request, res):
    "Edits request"
    req = validate_user_request(request, res)
    if not isinstance(req, Request):
        return req
    
    if request.method == "POST":
        pass
    # Dynamically set new widget
    edit_form    = RequestForm({"description": req.description})
    widget  = forms.Textarea(attrs={"rows": 3, "placeholder": "I want to see ...", "style": "width: 400px;"})
    del widget.attrs["cols"]
    edit_form.fields["description"].widget = widget
    
    c   = {
        "req":  req,
        "form": edit_form
    }
    c.update(csrf_token)
    
    resp    = {
        "data": render_to_string("forms/edit_request.html", c)
    }
    return http_response_json(resp)    
    

def remove_request_ajax(request, res):
    "Removes request"
    req = validate_user_request(request, res, True)
    if not isinstance(req, Request):
        return req
    
    return bad_request_json({"error": "Not implemented yet"})
    # XXX: Finish
    #if request.method != "POST":
    #    return bad_request_json({"error": "Invalid request method"})
    #try:
    #    result = WRequest.purge_request(res, req.user)
    #    return http_response_json({"data": "ok"})
    #except Exception, e:
    #    return bad_request_json({"error": str(e)})


def get_request_comments_json(request):
    "Returns paginated list of requests"
    res     = request.GET.get("request")
    if not res:
        return bad_request_json({"error": "Request parameter is not set"})
    
    try:
        req     = Request.objects.get(resource=res)
        coms    = RequestComment.objects.filter(request=req)
        paginator   = Paginator(coms, 2)   # 20 items per page
        page        = request.GET.get("page")        
        (items, page_num)   = paginated_items(paginator, page)
        
        paging  = {
            "page":     page_num,
            "total":    paginator.num_pages
        }
        comments    = []
        for rc in items:
            com = rc.comment
            comments.append({
                "text":     com.text,
                "username": com.user.username,
                "hdate":    ts2hd(com.submitted_date),
                "utcdate":  ts2utc(com.submitted_date)
            })
        data    = {
            "data": {
                "request":  res,
                "paging":   paging,
                "comments": comments
            }
        }
        
        return http_response_json(data)
    except Request.DoesNotExist, e:
        return bad_request_json({"error": str(e)})
    

@csrf_protect
def add_comment_json(request):
    "Adds comment"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    if request.method != "POST":
        return bad_request_json({"error": "Method is not supported"})
    
    try:
        res     = request.GET.get("request", None)
        req     = Request.objects.get(resource=res)
        user    = request.user
        
    except Request.DoesNotExist, e:
        return bad_request_json({"error": str(e)})
            
    c   = {
        "comment":  request.POST.get("comment", None)
    }
    form    = CommentForm(c)
    if not form.is_valid():
        return bad_form_json(form)

    # Create comment    
    text    = form.cleaned_data["comment"]
    
    # Can raise an exception
    com = WComment.add_comment(user, req, text)
    data    = {
        "text":     com.text,
        "username": com.user.username,
        "hdate":    ts2hd(com.submitted_date),
        "utcdate":  ts2utc(com.submitted_date),
        "request":  req.resource
    }
    return http_response_json({"data": data})
    

def get_profile(request):
    "Set profile"
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    
    return render(request, 'profile_general.html')  #


def edit_profile(request):
    "Edit profile"
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    
    return render(request, 'edit_profile.html')


def set_password(request):
    "Set password"
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    return render(request, 'profile_password.html')


def get_profile_photo(request):
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    
    user    = request.user
    im  = WImage.get_profile_image(user, "profile", "medium")
    photo_url   = im.url
    if not photo_url:
        photo_url   = "/media/img/user.png"
    c   = {
        "photo": photo_url
    }
    
    return render(request, 'profile_photo.html', c)    
    

def get_user(request, username):
    "Displays user profile"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
        user2       = userprof2.user
        
        c   = {
            "userprof2": userprof2,
            "is_you":    is_you(request, user2)
        }
    except UserProfile.DoesNotExist, e:
        logger.error("%s: %s" % (e, username))
        return render(request, 'misc/error_view.html', {"error": str(e)})
    
    if user2.first_name or user2.last_name:
        name   = "%s %s" % (user2.first_name, user2.last_name)
    else:
        name    = user2.username
    c["name"]   = name
    
    return render(request, 'user.html', c)


def users(request):
    "Returns list of users"
    usps        = UserProfile.objects.all()  # Filter by num of photos
    paginator   = Paginator(usps, 35)   # 35 items per page
    page        = request.GET.get("page")
    
    (items, page_num)   = paginated_items(paginator, page)
    c   = {
        "items":        items,
        "paginator":    paginator
    }
    return render(request, 'users.html', c)


def help(request):
    return render(request, 'help.html')


def _get_requests(request, reqs, c_ext = {}):
    paginator   = Paginator(reqs, 30)   # 30 items per page
    page        = request.GET.get("page")
    (items, page_num)   = paginated_items(paginator, page)
    c   = {
        "req_items":    TmplRequest.request_items(items),
        "items":        items,
        "paginator":    paginator
    }
    if c_ext and isinstance(c_ext, dict):
        c.update(c_ext)
    return render(request, 'requests.html', c)
    

def get_requests(request):
    "Returns list of requests"
    reqs    = WRequest.get_recent_requests()
    return _get_requests(request, reqs)


def get_location_requests(request, loc):
    "Returns requests for location which can be either city (City, State) or country"
    reqs    = WRequest.get_recent_requests()
    return _get_requests(request, reqs, {"title": "Requests For %s" % loc})
    

def get_user_requests_ajax(request, username):
    "Return user requests"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist, e:
        return bad_request_json({"error": str(e)})
    
    reqs    = Request.objects.filter(user=userprof2.user).order_by("-submitted_date")
    paginator   = Paginator(reqs, 10)   # 10 items per page
    page    = request.GET.get("page")
    
    (items, page_num)   = paginated_items(paginator, page)
    c   = {
        "req_items":    TmplRequest.request_items(items),
        "is_you":       is_you(request, userprof2.user),
        "paginator":    paginator
    }

    return http_response_json({"data": render_to_string("ajax/requests_list.html", c)})


def get_user_photos_ajax(request, username):
    "Return user photos"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist, e:
        return bad_request_json({"error": str(e)})

    (items, paginator)  = _get_photo_items(request)
    c   = {
        "items":        items,
        "is_you":       is_you(request, userprof2.user),
        "paginator":    paginator    
    }
    
    return http_response_json({"data": render_to_string("ajax/photos_list.html", c)})


def get_user_areas_ajax(request, username):
    "Return user areas"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist, e:
        return bad_request_json({"error": str(e)})
    
    return bad_request_json({"error": "Areas are not implemented yet"})
    
    
def get_user_comments_json(request, username):
    pass


def get_user_requests_json(request, username):
    "Returns user requests in json format"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist, e:
        return bad_request_json({"error": str(e)})
    
    reqs    = Request.objects.filter(user=userprof2.user).order_by("-submitted_date")
    paginator   = Paginator(reqs, 10)   # 10 items per page
    page    = request.GET.get("page")
    
    (items, page_num)   = paginated_items(paginator, page)
    req_items   = TmplRequest.request_items(items)
    data    = []
    for item in req_items:
        req = item.request
        data_item   = {
            "id":       req.id,
            "resource": req.resource,
            "title":    req.description if len(req.description) < 60 else "%s..." % req.description[:60],
            "description":  req.description,
            "thumb_url":    item.thumb_url,
            "street":   req.location.street,
            "city":     req.location.city,
            "username": username,
            "time_display": item.htime.human_time
        }
        data.append(data_item)
    c   = {
        "data":     data,
        "paging":   {
            "page":     page_num,
            "total":    paginator.num_pages
        },
        "total":    paginator.count
    }
    return http_response_json(c)


def recent_photos(request):
    "Returns list of photos"
    (items, paginator)  = _get_photo_items(request)
    c   = {
        "items":        items,
        "paginator":    paginator
    }
    return render(request, 'photos.html', c)


# XXX: Refactor to something else?
def _get_photo_items(request):
    "Returns photo request items and paginator"
    images  = Image.objects.filter(size_type="medium").filter(is_avail=True).order_by("-updated_time")
    phreqs  = PhotoRequest.objects.filter(photo__image__in=images).order_by("-photo__image__updated_time") # Same number as images length
    paginator   = Paginator(phreqs, 12)   # 12 items per page
    page    = request.GET.get("page")
    
    (paged_phreqs, page_num)   = paginated_items(paginator, page)
    paged_images    = images[:len(paged_phreqs)]
    return (zip(paged_images, paged_phreqs), paginator)    
    

def search(request):
    return render(request, 'search.html')

def search2(request):
    return render(request, 'search2.html')


TEMP_UP = """{% var file=o.files[0]; %}
{% if (file.error) { %}
    <div class="e-alert-head e-alert-inline alert-error pull-left" id="errors_container">
        {%=locale.fileupload.errors[file.error] || file.error%}
    </div>
{% } else if (o.files.valid) { %}
    <img src="/media/img/spinner_small.gif" class="e-button-spinner"/>
{% } %}
"""


def submit_select(request, res):
    "Displays file form or uploads file to S3"
    req = validate_user_request(request, res, False)
    if not isinstance(req, Request):
        return req
    
    user    = request.user  # User object
    
    if request.method == "POST":    # Ajax request
        # Upload image
        form   = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fd  = request.FILES["file"]
            try:
                # Note: Error messages are not really used here bacause of weird error handling in
                #       jQueryFileUpload widget
                
                format      = IMAGE_TYPES.get(fd.content_type, "err")
                filename    = s3key(res, "preview", format)
                img         = ImageFile(fd)     # convert to image
                
                # DB handling
                im  = WImage.get_or_create_image_by_request(user, req, "preview", marked_delete=True)
                im.name     = filename
                im.height   = img.height
                im.width    = img.width
                im.url      = s3_key2url(filename)
                im.size     = fd.size
                im.format   = format
                im.is_avail = s3_upload_file(fd, filename)
                im.save()
                
                # Send email notification?
                
                # Do I need to upload the file in chunks? Probably not if file is less than 5Mb
                return http_response_json([{"success": True, "url": s3_key2url(filename)}])
            
            except User.DoesNotExist:
                return bad_request_json({"error": "User does not exist"})
            except Exception, e:
                logger.debug(str(e))
                return bad_request_json([{"error": str(e)}])
        
        errors  = form.errors.items()
        msg     = "Something is wrong ..."
        if len(errors) != 0:
            msg = errors[0]
        return bad_request_json([{"error": msg}])

    # Display form
    c   = {
        "form":     UploadFileForm(),
        "resource": res,
        "temp_up":  TEMP_UP
    }
    return render(request, 'modals/submit_select.html', c)    
    

def submit_crop(request, res):
    "Displays crop form or crops uploaded image"
    req = validate_user_request(request, res, False)
    if not isinstance(req, Request):
        return req
    
    user    = request.user

    im  = WImage.get_image_by_request(req, "preview")
    if not im:
        return bad_request_json({"error": "Photo request doesn't exist"})
    
    if request.method == "POST":
        
        # Crop image
        crop_form   = CropForm(request.POST)
        if not crop_form.is_valid():
            # XXX: Test again, might be broken!
            return bad_form_json(crop_form)
        
        x   = int(crop_form.cleaned_data["x"])
        y   = int(crop_form.cleaned_data["y"])
        h   = int(crop_form.cleaned_data["h"])
        w   = int(crop_form.cleaned_data["w"])
        #if not (x and y and h and w):
        #    return HttpResponseRedirect("/submit2") # Error
        
        return handle_request_crop_file(req, user, im, (x, y, w, h))

    if im.width <= 460 and im.height <= 460:
        # No need to crop - upload directly
        result  = handle_request_crop_file(req, user, im, (0, 0, im.width, im.height))
        if isinstance(result, HttpResponseBadRequest):
            return result
        
        return HttpResponseRedirect("/submit/create/%s" % res)

    c   = {
        "crop_form":    CropForm(),
        "resource":     res,
        "img_src":      im.url,
        "img_width":    im.width,
        "img_height":   im.height
    }
    return render(request, 'modals/submit_crop.html', c)


def handle_request_crop_file(req, user, image, (x, y, w, h)):
    "Handles request crop file"
    res         = req.resource
    filename    = s3key(res, "crop", image.format)
    imc  = WImage.get_or_create_image_by_request(user, req, "crop", marked_delete=True)
    return handle_crop_file(imc, filename, image, (x, y, w, h))
    

def handle_profile_crop_file(user, image, (x, y, w, h)):
    "Handles profile crop file"
    filename    = s3key(user.username, "crop", image.format)
    imc  = WImage.get_or_create_profile_image(user, "crop", marked_delete=True)
    return handle_crop_file(imc, filename, image, (x, y, w, h))


def handle_crop_file(imc, filename, image, (x, y, w, h)):
    "Handles uploading crop file and manages db"
    try:
        imc.name     = filename
        imc.height   = h
        imc.width    = w
        imc.url      = s3_key2url(filename)            
        (imc.is_avail, imc.size)    = crop_s3_image(image.name, filename, (x, y, w, h))
        imc.format   = image.format
        imc.save()
    except Exception, e:
        return bad_request_json({"error": str(e)})
    
    return http_response_json({"success": True})    


def submit_create(request, res):
    "Creates images of different sizes"
    req = validate_user_request(request, res, False)
    if not isinstance(req, Request):
        return req
    
    user    = request.user

    imc  = WImage.get_image_by_request(req, "crop")
    if not imc:
        return bad_request_json({"error": "Photo request doesn't exist"})
    
    if request.method == "POST":
        try:
            file_base   = req.resource
            fmt     = imc.format
            # Populate image db records
            params  = ((460, "large"), (200, "medium"), (50, "small"))
            db_imgs = []
            for param in params:
                (size, size_type)   = param
                im  = WImage.get_or_create_image_by_request(user, req, "request", size_type)
                im.name = s3key(file_base, size_type, fmt)
                im.save()
                db_imgs.append((size, im))
            
            proc_images(file_base, db_imgs, fmt)
            return http_response_json({"success": True})
        except Exception, e:
            logger.debug(str(e))
            return bad_request_json({"error": str(e)})
        
    c   = {
        "resource":     res,
        "img_src":      imc.url
    }
    return render(request, 'modals/submit_create.html', c)    

# XXX: Refactor profile_photo_select() and submit_select()

def profile_photo_select(request):
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})   
    
    user    = request.user
    
    if request.method == "POST":    # Ajax request
        # Upload image
        form   = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fd  = request.FILES["file"]
            try:
                # Note: Error messages are not really used here bacause of weird error handling in
                #       jQueryFileUpload widget
                
                format      = IMAGE_TYPES.get(fd.content_type, "err")
                filename    = s3key(user.username, "preview", format)
                img         = ImageFile(fd)     # convert to image
                
                # DB handling
                im  = WImage.get_or_create_profile_image(user, "preview", marked_delete=True)
                im.name     = filename
                im.height   = img.height
                im.width    = img.width
                im.url      = s3_key2url(filename)
                im.size     = fd.size
                im.format   = format
                im.is_avail = s3_upload_file(fd, filename)
                im.save()
                
                # Send email notification?
                
                # Do I need to upload the file in chunks? Probably not if file is less than 5Mb
                return http_response_json([{"success": True, "url": s3_key2url(filename)}])
            
            except User.DoesNotExist:
                return bad_request_json({"error": "User does not exist"})
            except Exception, e:
                logger.debug(str(e))
                return bad_request_json([{"error": str(e)}])
        
        errors  = form.errors.items()
        msg     = "Something is wrong ..."
        if len(errors) != 0:
            msg = errors[0]
        return bad_request_json([{"error": msg}])

    # Display form
    c   = {
        "form":     UploadFileForm(),
        "temp_up":  TEMP_UP
    }
    return render(request, 'modals/submit_select.html', c)    


# XXX: Refactor profile_photo_crop() and submit_crop()

def profile_photo_crop(request):
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    user    = request.user

    im  = WImage.get_profile_image(user, "preview")
    if not im:
        return bad_request_json({"error": "Photo request doesn't exist"})
    
    if request.method == "POST":
        # Crop image
        crop_form   = CropForm(request.POST)
        if crop_form.is_valid():
            x   = int(crop_form.cleaned_data["x"])
            y   = int(crop_form.cleaned_data["y"])
            h   = int(crop_form.cleaned_data["h"])
            w   = int(crop_form.cleaned_data["w"])
            #if not (x and y and h and w):
            #    return HttpResponseRedirect("/submit2") # Error
            
            return handle_profile_crop_file(user, im, (x, y, w, h))
        
        errors  = crop_form.errors.items()
        msg     = "Something is wrong ..."
        if len(errors) != 0:
            msg = errors[0]
        return bad_request_json({"error": msg})
    
    if im.width <= 140 and im.height <= 140:
        # No need to crop - upload directly
        result  = handle_profile_crop_file(user, im, (0, 0, im.width, im.height))
        if isinstance(result, HttpResponseBadRequest):
            return result
        
        return HttpResponseRedirect("/profile/photo/create/%s" % res)
    
    c   = {
        "crop_form":    CropForm(),
        "img_src":      im.url,
        "img_width":    im.width,
        "img_height":   im.height
    }
    return render(request, 'modals/submit_crop.html', c)    

# XXX: Refactor profile_photo_create() and submit_create()

def profile_photo_create(request):
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})    
    user    = request.user

    imc     = WImage.get_profile_image(user, "crop")
    if not imc:
        return bad_request_json({"error": "Photo request doesn't exist"})
    
    if request.method == "POST":
        try:
            file_base   = user.username
            fmt     = imc.format
            # Populate image db records
            params  = ((140, "medium"), (50, "small"), (32, "tiny"))
            db_imgs = []
            for param in params:
                (size, size_type)   = param
                # get_or_create_profile_image(cls, user, photo_type, size_type=None, marked_delete=False, save=False):
                im  = WImage.get_or_create_profile_image(user, "profile", size_type)
                im.name = s3key(file_base, size_type, fmt)
                im.save()
                db_imgs.append((size, im))
            
            proc_images(file_base, db_imgs, fmt)
            
            return http_response_json({"success": True})
        except Exception, e:
            logger.debug(str(e))
            return bad_request_json({"error": str(e)})
        
    c   = {
        "img_src":      imc.url
    }
    return render(request, 'modals/submit_create.html', c)  


