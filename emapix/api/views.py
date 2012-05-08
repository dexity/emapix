from django.http import HttpResponse


def add(request):
    # lat, lon, resource
    return HttpResponse("Request")


def remove(request, reqid):
    return HttpResponse("Request:remove: %s" % reqid)


def get(request, reqid):
    return HttpResponse("Request:get: %s" % reqid)


def get_all(request):
    return HttpResponse("Request:get_all")


def update(request, reqid):
    # resource
    return HttpResponse("Request:update: %s" % reqid)

