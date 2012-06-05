from django.http import HttpResponse
from django.shortcuts import render_to_response

from emapix.utils.logger import Logger
logger = Logger.get("emapix.layout.views")

def index(request):
    return render_to_response('index.html')


def requests(request):
    return render_to_response('requests.html')
