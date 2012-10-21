from django.db import models
from django import forms

from emapix.exceptions import ServiceException
from emapix.core.models import *

class ObjectExists(object):
    
    def __init__(self, message, code, objects):
        self.objects    = objects
        self.message    = message
        self.code       = code
    
    def _get_items(self, value):
        raise Exception("Not implemented")
    
    def __call__(self, value):
        if not isinstance(self.objects, models.Manager):
            raise ServiceException("Object is invalid")

        items   = self._get_items(value)
        if len(items) > 0:
            raise forms.ValidationError(self.message, code=self.code)


class UsernameExists(ObjectExists):
    
    def _get_items(self, value):
        return self.objects.filter(username = value)


class EmailExists(ObjectExists):
    
    def _get_items(self, value):
        return self.objects.filter(email = value)
    

def validate_user_request_json(request, res):
    "Validates user and request. Returns json response if error or request"
    if not request.user.is_authenticated():
        return forbidden_json({"error": "You need to be logged in"})
    try:
        return Request.objects.get(resource=res)
    except Request.DoesNotExist:
        return bad_request_json({"error": "Request doesn't exist"})


    
