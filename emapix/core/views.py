import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User

from emapix.utils.const import *
from emapix.utils.utils import sha1
from emapix.core.forms import JoinForm
from emapix.core.models import UserProfile
from emapix.settings import NOREPLY_EMAIL

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.views")

def index(request):
    return render_to_response('index.html')


def generate_token(value):
    "Generates 40 character token"
    return sha1(value + str(time.time()))


def send_activation_email(request, email, username):
    "Send verification email"
    token   = generate_token(username)
    url     = "http://%s/confirm/%s" % (request.META["SERVER_NAME"], token)
    msg     = """
Hi, %s!

Please confirm your registration by following the link: %s

Explore the world!
Emapix Team

P.S. If you received this email by error, please ignore it.

""" % (username, url)

    send_mail('Verify registration', msg, NOREPLY_EMAIL, [email,], fail_silently=False)
    

@csrf_protect
def join(request):
    
    if request.method == "POST":
        form    = JoinForm(request.POST)
        if form.is_valid():
            username    = form.cleaned_data["username"]
            email       = form.cleaned_data["email"]
            password    = form.cleaned_data["password"]
            
            send_activation_email(request, email, username)
            # TEMP
            return HttpResponseRedirect("/verify")
            
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
            profile.save()
            
            send_activation_email(request, email, username)
            
            #return HttpResponseRedirect("/confirm")
            return HttpResponseRedirect("/verify")
    else:
        form    = JoinForm()

    c   = {
        "form":     form
    }
    return render(request, "join.html", c)


def verify(request):
    return render(request, "message.html", {"type": "verify"})


def confirm(request, token):
    # Check user token
    logger.debug(token)
    #return render_to_response('confirm.html')

def login(request):
    
    return render_to_response('login.html')

def forgot(request):
    return render_to_response('forgot.html')

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
    return render_to_response('requests.html')

def request(request):
    return render_to_response('request.html')

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

def make(request):
    return render_to_response('make.html')



