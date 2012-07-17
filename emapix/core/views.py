from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
from emapix.utils.const import *
from emapix.core.forms import JoinForm

from django.db import models

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.views")

def index(request):
    return render_to_response('index.html')

@csrf_protect
def join(request):
    
    if request.method == "POST":
        form    = JoinForm(request.POST)
        if form.is_valid():
            username    = form.cleaned_data["username"]
            # ...
            return HttpResponseRedirect("/confirm")
    else:
        form    = JoinForm()

    c   = {
        "form":     form
    }
    return render(request, "join.html", c)

def confirm(request):
    return render_to_response('confirm.html')

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



