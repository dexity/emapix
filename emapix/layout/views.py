from django.http import HttpResponse
from django.shortcuts import render_to_response

from emapix.utils.logger import Logger
logger = Logger.get("emapix.layout.views")

def index(request):
    return render_to_response('index.html')

def join(request):
    return render_to_response('join.html')

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


