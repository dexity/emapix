import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import models
from django.contrib.auth.models import User
import django.contrib.auth as django_auth

from emapix.utils.const import *
from emapix.utils.utils import sha1, random16, timestamp
from emapix.utils.format import *
from emapix.core.forms import *
from emapix.core.models import *
from emapix.core.emails import send_activation_email, send_forgot_email, send_newpass_confirm_email

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.views")

def index(request):
    return render_to_response("index.html")


def generate_token(value):
    "Generates 40 character token"
    return sha1(value + str(time.time()))
    

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
            # Create Request
            p   = request.POST
            r   = Request()
            r.user  = _user
            r.lat   = 1e6*form.cleaned_data["lat"]
            r.lon   = 1e6*form.cleaned_data["lon"]
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
        c["lat"]    = req.lat/1e6
        c["lon"]    = req.lon/1e6
        c["description"]    = req.description
        c["resource"]   = req.resource

    return render(request, 'ajax/request_info.html', c)


def get_request(request, res):
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}
    return render(request, 'request.html', c)


def remove_request(request, res):
    "Removes request"
    if not request.user.is_authenticated():
        return render(request, 'ajax/error.html', {"error": AUTH_ERROR})
    
    if request.method != "POST":
        return render(request, 'ajax/error.html', {"error":  "Invalid request" })
    try:
        req     = Request.objects.get(resource=res)
        req.delete()
        return to_status(OK)
    except Exception, e:
        return render(request, 'ajax/error.html', {"error":  "Request does not exist"})



def set_profile(request):
    return render_to_response('set_profile.html')

def set_password(request):
    return render_to_response('set_password.html')

def profile(request):
    return render_to_response('profile.html')

def users(request):
    return render_to_response('users.html')

def help(request):
    return render_to_response('help.html')


def requests(request):
    if request.user.is_authenticated():
        c   = {"username": request.user}
    else:
        c   = {}    
    return render(request, 'requests.html', c)


def request2(request):
    return render_to_response('request2.html')

def photos(request):
    return render_to_response('photos.html')

def search(request):
    return render_to_response('search.html')

def search2(request):
    return render_to_response('search2.html')

def submit(request):
    return render_to_response('submit.html')

def submit2(request):
    return render_to_response('submit2.html')

def submit3(request):
    return render_to_response('submit3.html')



