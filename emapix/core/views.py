
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

from constance import config

from emapix.utils.const import *
from emapix.utils.utils import sha1, random16, timestamp, ts2h, ts2utc, ts2hd, bad_request_json, \
http_response_json, forbidden_json, s3key, paginated_items, is_you, bad_form_json, server_error_json

from emapix.core.validators import validate_user_request, validate_user_comment, OtherEmailExists    #, validate_user
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
from emapix.core.db.user import WUser
from emapix.core.db.photo import WPhoto
from emapix.core.tmpl.request import TmplRequest
from emapix.core.tmpl.image import TmplImage
from emapix.core.forms import RecaptchaForm

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.views")


def generate_token(value):
    "Generates 40 character token"
    return sha1(value + str(time.time()))
    

@csrf_protect
def join(request):
    "Submits registration form and sends activation email"
    clean_join_session(request)
    
    # For authenticated user join form is not displayed
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        form    = JoinForm(request.POST)
        if not form.is_valid():
            c   = {
                "form":     form,
                "hide_join":    True
            }
            return render(request, "join.html", c)
            
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

    c   = {
        "form":     JoinForm(),
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

            # Creates user
            try:
                user        = User()
                user.username = username
                user.email  = email
                user.set_password(join_session["password"])
                user.is_active  = False
                user.save()
            except Exception, e:
                logger.error("User create error: %s" % e)
                clean_join_session(request)
                c   = {
                    "error": "New user account can't be created at this time. Please try again later"
                }
                return render(request, "misc/error_view.html", c)
            
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
            logger.info("New user: %s" % username)
            
            # Redirect to welcome page
            request.session["joined"]   = True
            return HttpResponseRedirect("/welcome")

    c   = {
        "form":  form,
        "hide_join":    True
    }
    return render(request, "recaptcha.html", c)


def welcome(request):
    "Redirects to welcome page"
    if request.session.has_key("joined") and request.session["joined"]:
        del request.session["joined"]
        c   = {
            "hide_join": True,
            "msg":      render_to_string("msg/verify.html")
        }
        return render(request, "message.html", c)
    return HttpResponseRedirect("/")


def success(request, redirect_path="/"):
    "Success redirection"
    try:
        c   = {
            "hide_join": True,
            "msg":  render_to_string(request.session["msg_tmpl"])
        }
        del request.session["msg_tmpl"]
        return render(request, "message.html", c)
    except Exception, e:
        pass

    return HttpResponseRedirect(redirect_path)


def clean_join_session(request):
    "Remove join session"
    try:
        del request.session["join"]
    except KeyError:
        pass
    

def confirm(request, token):
    # Check user token
    c   = {
        "hide_join":    True
    }
    try:
        profile = UserProfile.objects.get(activ_token = token)
        profile.user.is_active  = True
        profile.user.save()
        profile.activ_token = None
        profile.save()
        c["msg"]    = render_to_string("msg/confirm.html")
    except Exception, e:
        logger.error("Activation failed: %s" % e)
        c["msg"]    = render_to_string("msg/confirm_failed.html")

    return render(request, "message.html", c)


@csrf_protect
def login(request):
    "Loggs user in"
    c   = {
        "hide_join":    True
    }
    if request.method == "POST":
        form    = LoginForm(request.POST)
        if not form.is_valid():
            c["form"]   = form
            return render(request, 'login.html', c)
        
        # Should have user authenticated already
        django_auth.login(request, form.cleaned_data["user"])   
        return HttpResponseRedirect("/")

    c["form"]   = LoginForm()
    return render(request, 'login.html', c)


def logout(request):
    "Loggs user out"
    django_auth.logout(request)
    return HttpResponseRedirect("/")


def verify_resend(request):
    "Sends verification token again"
    c   = {
        "hide_join":    True
    }       
    if request.method == "POST":
        form    = ResendForm(request.POST)
        if not form.is_valid():
            c["form"]   = form
            return render(request, "resend.html", c)
        
        # Should be set by now
        prof    = form.cleaned_data["user_profile"]
        # Send activation email again
        send_activation_email(request, prof.user.email, prof.user.username, prof.activ_token)
        request.session["msg_tmpl"]  = "msg/verify_resend.html"
        return HttpResponseRedirect("/success")
    
    c["form"]   = ResendForm()
    return render(request, "resend.html", c)


@csrf_protect
def forgot(request):
    "Handles forgot request"
    c   = {
        "hide_join":    True
    }    
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
                
                request.session["msg_tmpl"] = "msg/forgot.html"
                return HttpResponseRedirect("/success")
            except Exception, e:
                logger.error("Forgot form failed: %s" % e)
        c["form"]   = form
        return render(request, 'forgot.html', c)        

    c["form"]   = ForgotForm()
    return render(request, 'forgot.html', c)


@csrf_protect
def renew_password(request, token):
    "Renews password"
    
    # For authenticated user renew form is not displayed
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    c   = {
        "hide_join":    True,
        "submit_btn":   "Create New Password"
    }
    try:
        profile = UserProfile.objects.get(forgot_token = token)
    except Exception, e:
        logger.error("Renew password failed: %s" % e)
        c["msg"]    = render_to_string("msg/newpass_failed.html")
        return render(request, "message.html", c)
    
    if request.method == "POST":
        form    = NewPasswordForm(request.POST)
        if not form.is_valid():
            c["form"]   = form
            c["token"]  = token
            return render(request, "newpass.html", c)
        
        newpass = form.cleaned_data["passone"]
        profile.forgot_token = ""
        profile.user.set_password(newpass)
        profile.user.save() # Important
        profile.save()
        
        email   = profile.user.email
        username    = profile.user.username
        # Send email
        send_newpass_confirm_email(request, email, username)
        c["msg"]    = render_to_string("msg/newpass_success.html")
        return render(request, "message.html", c)

    c["form"]   = NewPasswordForm()
    c["token"]  = token
    return render(request, "newpass.html", c)


def make_request(request):
    "Makes request"
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})    
    c   = {
        "map_key":  config.map_key
    }
    return render(request, 'make.html', c)


@csrf_protect
def add_request(request):
    "Displays and handles photo request form on the map"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    
    user    = request.user
    try:
        prof    = UserProfile.objects.get(user=user)
    except Exception, e:
        return bad_request_json({"error": str(e)})
    
    if request.method == "POST":
        form    = RequestForm(request.POST)
        if not form.is_valid():
            return bad_form_json(form)
        
        lat = form.cleaned_data["lat"]
        lon = form.cleaned_data["lon"]
        
        # Create Location
        l   = Location()
        l.lat   = 1e6*lat
        l.lon   = 1e6*lon
        
        # Set address (to separate function)
        addr    = latlon2addr(lat, lon)
        if addr is not None:
            (l.res_lat, l.res_lon)   = addr[0]
            (l.street, l.city, l.country) = addr[1]
            l.res_type  = addr[2]
            l.zipcode   = addr[3]
            
        l.save()
        
        # Create Request
        r   = Request()
        r.user  = user
        r.location  = l
        r.description   = form.cleaned_data["description"]
        r.resource  = random16()
        r.save()
        
        data    = {
            "data": to_request(r)
        }
        return http_response_json(data)
    
    # GET request
    lat = request.GET.get("lat", "")
    lon = request.GET.get("lon", "")
    form    = RequestForm(initial={"lat": lat, "lon": lon})

    # Check daily limit
    reqs    = WRequest.get_recent_requests(user=user, days=1, recent=False)
    overhead = reqs.count() - prof.req_limit
    if overhead > 0:
        return forbidden_json({"error": "Daily quota of %s requests is reached" % prof.req_limit})
    
    c   = {
        "lat":  lat,
        "lon":  lon,
        "form": form
    }
    c.update(csrf(request))
    
    resp    = {
        "data": render_to_string("forms/request_form.html", c)
    }
    return http_response_json(resp)


def get_requests_json(request):
    "Returns list of all user's markers"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    
    user    = request.user
    reqs    = Request.objects.filter(user=user)
    data    = {
        "data": to_requests(reqs)
    }
    return http_response_json(data)


def request_info(request, res):
    "Displays the request info"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    
    try:
        req     = Request.objects.get(resource=res)
        img     = WImage.get_image_by_request(req, size_type="medium")
    except Exception, e:
        return bad_request_json({"error": str(e)})

    c   = {
        "req":  req,
        "img":  img
    }
    c.update(csrf(request))
    data    = {
        "data":     render_to_string("ajax/request_info.html", c)
    }
    return http_response_json(data)


def get_request(request, res):
    "Returns request"
    try:
        req = Request.objects.get(resource=res)
        req.location.lat    = req.location.lat/1e6
        req.location.lon    = req.location.lon/1e6
        img     = WImage.get_image_by_request(req, size_type="large")
        photo   = WPhoto.photo_by_request(res)
        
        c   = {
            "req":      req,
            "is_open":  req.status == "o",
            "req_auth": is_you(request, req.user),
            "hdate":    ts2hd(req.submitted_date),
            "utcdate":  ts2utc(req.submitted_date),
            "map_key":  config.map_key
        }
        if isinstance(photo, Photo) and not photo.marked_delete:
            c["submitter"]  = photo.user
            # Request owner or photo owner has access to submitted photo
            c["pic_auth"]   = c["req_auth"] or is_you(request, photo.user)
            c["photo"]      = photo
            c["pic_hdate"]  = ts2hd(photo.created_time)
            c["pic_utcdate"]    = ts2utc(photo.created_time)
            if isinstance(img, Image): #and img.is_avail:
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
        form    = RequestForm(request.POST)
        form.fields["lat"].required = False
        form.fields["lon"].required = False
        if not form.is_valid():
            return bad_form_json(form)
        
        try:
            req.description = form.cleaned_data["description"]
            req.save()
        except Exception, e:
            return server_error_json({"error": str(e)})
        return to_ok()
    
    # Dynamically set new widget
    form    = RequestForm({"description": req.description})
    widget  = forms.Textarea(attrs={"rows": 3, "placeholder": "I want to see ...", "style": "width: 400px;"})
    del widget.attrs["cols"]
    form.fields["description"].widget = widget
    
    c   = {
        "req":  req,
        "form": form
    }
    c.update(csrf(request))
    
    resp    = {
        "data": render_to_string("forms/edit_request.html", c)
    }
    return http_response_json(resp)    
    
    
def request_status_ajax(request, res, status):
    "Change status of the request"
    req = validate_user_request(request, res)   # Only owner can change the request status
    if not isinstance(req, Request):
        return req
    
    status  = SHORT_REQ_STATUS.get(status, None)
    if status not in [x[0] for x in REQ_STATUS_CHOICES]:
        return bad_request_json({"error": "Parameter status is not valid"})    
    
    try:
        req.status  = status
        req.save()
        return http_response_json({"data": "ok"})
    except Exception, e:
        return server_error_json({"error": str(e)})
    

@csrf_protect
def remove_request_photo_ajax(request, res):
    "Marks request photo for removal. Used in request view"
    req = validate_user_request(request, res, False)
    if not isinstance(req, Request):
        return req
    
    rph   = WPhoto.request_photo(res)
    if not (rph and rph.photo):
        return bad_request_json({"error": "Photo does not exist"})
    
    photo   = rph.photo
    # Only photo owner or request owner can remove the photo
    if not (is_you(request, photo.user) or is_you(request, req.user)):
        return forbidden_json({"error": AUTHOR_ERROR})

    if request.method == "POST":
        WPhoto.remove_photo(res)
        return to_ok()
    
    c   = {}
    c.update(csrf(request))
    resp   = {
        "data":     render_to_string("forms/remove_photo_form.html", c)
    }
    return http_response_json(resp)


@csrf_protect
def remove_photo_json(request, photo_id):
    "Marks request photo for removal. Used in user view"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR})

    try:
        photo   = Photo.objects.get(id=photo_id)
        if photo.user != request.user:  # Only 
            return forbidden_json({"error": AUTHOR_ERROR})
    except Photo.DoesNotExist:
        return bad_request_json({"error": "Photo does not exist"})
    
    if request.method == "POST":
        try:
            phreq   = PhotoRequest.objects.get(photo=photo)
            WPhoto.remove_photo(phreq.request.resource)
        except Exception, e:
            return server_error_json({"error": str(e)})
        return to_ok()
    
    c   = {}
    c.update(csrf(request))
    resp    = {
        "data": render_to_string("forms/remove_photo_form.html", c)
    }
    return http_response_json(resp)    


@csrf_protect
def remove_request_ajax(request, res):
    "Removes request"
    req = validate_user_request(request, res, True)
    if not isinstance(req, Request):
        return req

    if request.method == "POST":
        try:
            result = WRequest.purge_request_or_raise(res, req.user)
            return to_ok()
        except Exception, e:
            return bad_request_json({"error": str(e)})
    
    c   = {}
    c.update(csrf(request))
    resp    = {
        "data": render_to_string("forms/remove_request_form.html", c)
    }
    return http_response_json(resp)


# XXX: Refactor to format.py
def to_request2(req, desc_size=None):
    "Returns request dictionary"
    desc    = req.description
    if isinstance(desc_size, int):
        desc    = desc[:desc_size]
    return {"resource":     req.resource,
            "description":  req.description if len(req.description) < desc_size else "%s..." % req.description[:desc_size]
            }


def get_comments(request, req=None, userprof=None, num_pages=10, recent_first=False):
    "Util that returns comments in json format both for request and user profile"
    coms    = RequestComment.objects
    if req:
        coms    = coms.filter(request=req)
    elif userprof:
        coms    = coms.filter(comment__user=userprof.user)
    else:
        raise Exception("Either Request or User objects has to be set")
    if recent_first:
        coms    = coms.order_by("-comment__submitted_date")
    else:
        coms    = coms.order_by("comment__submitted_date")
    paginator   = Paginator(coms, num_pages)
    page        = request.GET.get("page", 1)        
    (items, page_num)   = paginated_items(paginator, page)
    
    paging  = {
        "page":     page_num,
        "total":    paginator.num_pages
    }
    comments    = []
    for rc in items:
        com = rc.comment
        (sd, ct)  = (int(com.submitted_date), timestamp())
        comdict = {
            "id":       com.id,
            "text":     com.text,
            "username": com.user.username,
            "hdate":    ts2h(sd, ct),
            "utcdate":  ts2utc(com.submitted_date)
        }
        if userprof:
            comdict["remove_url"]   = "/comment/%s/remove/json" % com.id
            comdict["request"]  = to_request2(rc.request, desc_size=50)
        comments.append(comdict)
    if req:
        com_total   = req.num_comments
    else:
        com_total   = userprof.num_comments
    data    = {
        "data": {
            "paging":   paging,
            "comments_total": com_total,
            "comments": comments
        }
    }
    if req:
        data["data"]["request"] =  to_request2(req)
    
    return http_response_json(data)    


def get_request_comments_json(request):
    "Returns paginated list of requests"
    res     = request.GET.get("request")
    if not res:
        return bad_request_json({"error": "Request parameter is not set"})
    
    try:
        req     = Request.objects.get(resource=res)
        return get_comments(request, req=req, num_pages=10)
    except Exception, e:    # Request.DoesNotExist
        return bad_request_json({"error": str(e)})
    

@csrf_protect
def add_comment_json(request):
    "Adds comment to the request"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    if request.method != "POST":
        return bad_request_json({"error": METHOD_ERROR})
    
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
    comment    = {
        "text":     com.text,
        "username": com.user.username,
        "hdate":    ts2hd(com.submitted_date),
        "utcdate":  ts2utc(com.submitted_date),
        "request":  req.resource
    }
    data    = {
        "comments_total":   req.num_comments,
        "comment":  comment
    }
    return http_response_json({"data": data})


def remove_comment_json(request, comment_id):
    "Removes comment"
    com     = validate_user_comment(request, comment_id, True)
    if not isinstance(com, Comment):
        return com
    
    if request.method == "POST":
        try:
            WComment.remove_comment(com.id)
        except Exception, e:
            return bad_request_json({"error": str(e)})
        return to_ok()
    
    c   = {}
    c.update(csrf(request))
    resp    = {
        "data": render_to_string("forms/remove_comment_form.html", c)
    }
    return http_response_json(resp)      
    

def get_profile(request):
    "Set profile"
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    
    """
    TODO:
        Add tab "Privacy" with the parameters:
        - "General":
            - "Show email"
        - "Profile"
            - "View requests"
            - "View photos"
            - "View comments"
    """
    try:
        userprof    = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, 'misc/error_view.html', {"error": "User does not exist"})
    c   = {
        "userprof": userprof
    }
    return render(request, 'profile_general.html', c)


@csrf_protect
def edit_profile(request):
    "Edit profile"
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    try:
        userprof    = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, 'misc/error_view.html', {"error": "User does not exist"})
    
    user    = request.user
    c   = {
        "user": user
    }
    if request.method == "POST":
        form    = ProfileForm(request.POST)
        email_valid = OtherEmailExists("Email already exists",
                                    "email_exists",
                                    User.objects,
                                    orig_email = user.email)
        form.fields["email"].validators = [email_valid]
        if form.is_valid():
            fcd  = form.cleaned_data
            try:
                user.first_name = fcd["first_name"]
                user.last_name  = fcd["last_name"]
                user.email      = fcd["email"]
                user.save()
                userprof.user       = user
                userprof.location   = fcd["location"]
                userprof.country_alpha2 = fcd["country"]
                b_day   = fcd["b_day"]
                if not b_day:
                    b_day   = None
                userprof.b_day      = b_day
                userprof.b_month    = fcd["b_month"]
                userprof.b_year     = fcd["b_year"]
                userprof.gender     = fcd["gender"]
                userprof.description    = fcd["description"]
                userprof.show_email = fcd["show_email"]
                userprof.show_location  = fcd["show_location"]
                userprof.show_birthday  = fcd["show_birthday"]
                userprof.show_gender    = fcd["show_gender"]
                userprof.save()
                return HttpResponseRedirect("/profile")
            except Exception, e:
                logger.error("Profile edit failed: %s" % e)
        
        c["form"]   = form
        return render(request, 'edit_profile.html', c)

    data    = {
        "first_name":   user.first_name,
        "last_name":    user.last_name,
        "email":        user.email,
        "location":     userprof.location,
        "country":      userprof.country_alpha2,
        "b_day":        userprof.b_day,
        "b_month":      userprof.b_month,
        "b_year":       userprof.b_year,
        "gender":       userprof.gender,
        "description":  userprof.description,
        "show_email":   userprof.show_email,
        "show_location":   userprof.show_location,
        "show_birthday":   userprof.show_birthday,
        "show_gender":   userprof.show_gender,
    }
    c["form"]   = ProfileForm(data)
    return render(request, 'edit_profile.html', c)


def update_password(request):
    "Update password"
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    form    = UpdatePasswordForm()
    form.fields["passone"].label    = "Original Password"
    form.fields["passtwo"].label    = "New Password"
    
    c   = {
        "form": form,
        "submit_btn":   "Save Changes"
    }
    user    = request.user
    if request.method == "POST":
        form.data   = request.POST
        form.is_bound   = True
        pass_valid  = ValidPassword("The password is not valid", "valid_password", user)
        form.fields["passone"].validators.append(pass_valid)
        if not form.is_valid():
            c["form"]   = form
            return render(request, "profile_password.html", c)
        
        origpass = form.cleaned_data["passone"]
        newpass  = form.cleaned_data["passtwo"]
        user.set_password(newpass)
        user.save()
        
        email       = user.email
        username    = user.username
        # Send email
        send_newpass_confirm_email(request, email, username)
        return HttpResponseRedirect("/profile")
    
    return render(request, "profile_password.html", c)


def get_profile_photo(request):
    if not request.user.is_authenticated():
        return render(request, 'misc/error_view.html', {"error": AUTH_ERROR})
    
    (photo_url, photo_exists)  = WImage.get_profile_image_meta(request.user)
    c   = {
        "photo_url":    photo_url,
        "photo_exists": photo_exists
    }
    
    return render(request, 'profile_photo.html', c)    
    

@csrf_protect
def remove_profile_photo_json(request):
    "Removes profile photo"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR})    
    if request.method != "POST":
        return bad_request_json({"error": "Invalid request method"})
    try:
        status  = WPhoto.remove_profile_photo(request.user)
        if status is False:
            return bad_request_json({"error": "Error removing the profile photo"})
    except Exception, e:
        return bad_request_json({"error": str(e)})

    return to_ok()
    

def get_user(request, username, tab="requests"):
    "Displays user profile"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
        user2       = userprof2.user
        
        (photo_url, photo_exists)   = WImage.get_profile_image_meta(user2)
        c   = {
            "userprof2":    userprof2,
            "photo_url":    photo_url,
            "photo_exists": photo_exists,
            "is_you":       is_you(request, user2)
        }
    except UserProfile.DoesNotExist, e:
        return render(request, 'misc/error_view.html', {"error": str(e)})

    if tab in ["requests", "photos", "comments"]:
        c["active"]  = tab
    
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
    photo_urls  = []
    for item in items:
        (photo_url, photo_exists)   = WImage.get_profile_image_meta(item.user, size_type="small",
                                                                    default_url="/media/img/small.png")
        photo_urls.append(photo_url)

    c   = {
        "items":        items,
        "photo_urls":   photo_urls,
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
    # Not currently used
    reqs    = WRequest.get_recent_requests()
    return _get_requests(request, reqs, {"title": "Requests For %s" % loc})


def get_user_areas_json(request, username):
    "Return user areas"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist, e:
        return bad_request_json({"error": str(e)})
    
    return bad_request_json({"error": "Areas are not implemented yet"})
    
    
def get_user_comments_json(request, username):
    "Returns user comments"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR})
    
    try:
        userprof2    = UserProfile.objects.get(user__username=username)
    except Exception, e:
        return bad_request_json({"error": str(e)})

    return get_comments(request, userprof=userprof2, num_pages=10, recent_first=True)    


def get_user_photos_json(request, username):
    "Return user photos"
    try:
        userprof2   = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist, e:
        return bad_request_json({"error": str(e)})

    # Refactor to db?
    phreqs      = PhotoRequest.objects.filter(photo__type="request")\
                  .exclude(photo__marked_delete=True) \
                  .filter(photo__user=userprof2.user)\
                  .order_by("-photo__updated_time")    
    paginator   = Paginator(phreqs, 12)   # 12 items per page
    page        = request.GET.get("page")
    
    (paged_phreqs, page_num)   = paginated_items(paginator, page)
    photos  = []
    for phreq in paged_phreqs:
        image   = WImage.get_image_by_photo(phreq.photo, size_type="medium")
        photo   = {
            "id":       phreq.photo.id,
            "request":  to_request2(phreq.request, 40),
            "location": {
                "city":     phreq.request.location.city,
                "country":  phreq.request.location.country
            },
            "image_url":    image.url
        }
        if is_you(request, userprof2.user):
            photo["remove_url"] = "/photo/%s/remove/json" % phreq.photo.id
        photos.append(photo)
    
    data    = {
        "data": {
            "photos":   photos,
            "photos_total": phreqs.count(),
            "paging":   {
                "total":    paginator.num_pages,
                "page":     page_num
            }
        }
    }
    return http_response_json(data)


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
            "location": {
                "street":   req.location.street,
                "city":     req.location.city,
                "lat":      req.location.lat/1e6,
                "lon":      req.location.lon/1e6,
                "country":  req.location.country
            },
            "username": username,
            "utcdate":  item.htime.utc_time,
            "hdate":    item.htime.human_time
        }
        if is_you(request, userprof2.user):
            data_item["remove_url"] = "/request/%s/remove/json" % req.resource
        data.append(data_item)
    
    c   = {
        "data":     {
            "paging":   {
                "page":     page_num,
                "total":    paginator.num_pages
            },
            "requests_total":    paginator.count,
            "requests": data
        }
    }
    return http_response_json(c)


def recent_photos(request):
    "Returns list of photos"
    phreqs      = PhotoRequest.objects.filter(photo__type="request")\
                  .exclude(photo__marked_delete=True) \
                  .order_by("-photo__updated_time")    
    paginator   = Paginator(phreqs, 12)   # 12 items per page
    page        = request.GET.get("page")
    
    (paged_phreqs, page_num)   = paginated_items(paginator, page)
    images  = []
    for phreq in paged_phreqs:
        image   = WImage.get_image_by_photo(phreq.photo, size_type="medium")
        images.append(image)
        
    c   = {
        "items":        paged_phreqs,
        "images":       images,
        "paginator":    paginator
    }
    return render(request, 'photos.html', c)


def search(request):
    return render(request, 'search.html')


def search2(request):
    return render(request, 'search2.html')


@csrf_protect
def submit_select(request, res):
    "Displays file form or uploads file to S3"
    req = validate_user_request(request, res, False)    # Anyone can submit photo
    if not isinstance(req, Request):
        return req
    
    user    = request.user  # User object
    
    if request.method == "POST":    # Ajax request
        # Upload image
        form   = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return bad_form_json(form)
        
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
            logger.error("Error uploading request (%s) photo preview: %s" % (res, e))
            return bad_request_json([{"error": str(e)}])

    # Display form
    c   = {
        "form":     UploadFileForm(),
        "resource": res
    }
    c.update(csrf(request))
    resp    = {
        "data":     render_to_string("modals/submit_select.html", c)
    }
    return http_response_json(resp)    
    

@csrf_protect
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
        
        return HttpResponseRedirect("/submit/create/%s?redirect=true" % res)

    c   = {
        "crop_form":    CropForm(),
        "resource":     res,
        "img_src":      im.url,
        "img_width":    im.width,
        "img_height":   im.height
    }
    c.update(csrf(request))
    
    resp    = {
        "data":     render_to_string("modals/submit_crop.html", c)
    }
    return http_response_json(resp)


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
    
    return to_ok()   


@csrf_protect
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
            return to_ok()
        except Exception, e:
            logger.error("Error uploading request (%s) photo: %s" % (res, e))
            return bad_request_json({"error": str(e)})
    
    c   = {
        "resource":     res,
        "img_src":      imc.url
    }
    c.update(csrf(request))
    resp    = {
        "data":     render_to_string("modals/submit_create.html", c),
        "redirect": request.GET.get("redirect", None) == "true"
    }
    return http_response_json(resp)


# XXX: Refactor profile_photo_select() and submit_select()
@csrf_protect
def profile_photo_select(request):
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})   
    
    user    = request.user
    
    if request.method == "POST":    # Ajax request
        # Upload image
        form   = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return bad_form_json(form)
        
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
            logger.error("Error uploading profile photo preview: %s" % e)
            return bad_request_json([{"error": str(e)}])

    # Display form
    c   = {
        "form":     UploadFileForm()
    }
    c.update(csrf(request))
    resp    = {
        "data":     render_to_string("modals/submit_select.html", c)
    }
    return http_response_json(resp)    


# XXX: Refactor profile_photo_crop() and submit_crop()
@csrf_protect
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
        if not crop_form.is_valid():
            return bad_form_json(crop_form)
        
        x   = int(crop_form.cleaned_data["x"])
        y   = int(crop_form.cleaned_data["y"])
        h   = int(crop_form.cleaned_data["h"])
        w   = int(crop_form.cleaned_data["w"])
        #if not (x and y and h and w):
        #    return HttpResponseRedirect("/submit2") # Error
        
        return handle_profile_crop_file(user, im, (x, y, w, h))
    
    if im.width <= 140 and im.height <= 140:
        # No need to crop - upload directly
        result  = handle_profile_crop_file(user, im, (0, 0, im.width, im.height))
        if isinstance(result, HttpResponseBadRequest):
            return result
        
        return HttpResponseRedirect("/profile/photo/create/%s?redirect=true" % res)
    
    c   = {
        "crop_form":    CropForm(),
        "img_src":      im.url,
        "img_width":    im.width,
        "img_height":   im.height
    }
    c.update(csrf(request))
    resp    = {
        "data":     render_to_string("modals/submit_crop.html", c)
    }
    return http_response_json(resp)   

# XXX: Refactor profile_photo_create() and submit_create()
@csrf_protect
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
            
            return to_ok()
        except Exception, e:
            logger.error("Error uploading profile photo: %s" % e)
            return bad_request_json({"error": str(e)})
        
    c   = {
        "img_src":      imc.url
    }
    c.update(csrf(request))
    resp    = {
        "data":     render_to_string("modals/submit_create.html", c),
        "redirect": request.GET.get("redirect", None) == "true"
    }
    return http_response_json(resp)


