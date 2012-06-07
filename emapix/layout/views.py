from django.http import HttpResponse
from django.shortcuts import render_to_response

from emapix.utils.logger import Logger
logger = Logger.get("emapix.layout.views")

def index(request):
    return render_to_response('index.html')

def requests(request):
    return render_to_response('requests.html')

def request(request):
    return render_to_response('request.html')

def requests2(request):
    return render_to_response('requests2.html')

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


