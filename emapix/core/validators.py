from django.db import models
from django import forms

from emapix.exceptions import ServiceException
from emapix.core.models import *
from emapix.utils.utils import bad_request_json, forbidden_json

from emapix.utils.const import *

class ObjectExists(object):
    
    def __init__(self, message, code, objects, **kwargs):
        self.objects    = objects
        self.message    = message
        self.code       = code
        self.kwargs     = kwargs
    
    def _get_items(self, value, **kwargs):
        raise Exception("Not implemented")
    
    def __call__(self, value):
        if not isinstance(self.objects, models.Manager):
            raise ServiceException("Object is invalid")

        items   = self._get_items(value, **self.kwargs)
        if items.exists():
            raise forms.ValidationError(self.message, code=self.code)


class UsernameExists(ObjectExists):
    
    def _get_items(self, value):
        return self.objects.filter(username = value)


class EmailExists(ObjectExists):
    
    def _get_items(self, value):
        return self.objects.filter(email = value)
    
    
class OtherEmailExists(ObjectExists):
    
    def _get_items(self, value, **kwargs):
        if not kwargs.has_key("orig_email"):
            raise forms.ValidationError("Service error: orig_email is required")
        return self.objects.exclude(email = kwargs["orig_email"]).filter(email = value)


class ValidPassword(object):
    
    def __init__(self, message, code, user):
        self.message    = message
        self.code       = code        
        self.user       = user
        
    def __call__(self, value):
        if not self.user.check_password(value):
            raise forms.ValidationError(self.message, self.code)


#def validate_user(request):
#    "Validates user and request. Returns json response if error or request"
#    if not request.user.is_authenticated():
#        return forbidden_json({"error": "You need to be logged in"})
#    return True


def validate_user_request(request, res, is_you=True):
    "Validates user and request. Returns json response if error or request"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    try:
        req = Request.objects.get(resource=res)
    except Request.DoesNotExist:
        return bad_request_json({"error": "Request doesn't exist"})
    if is_you and request.user != req.user:
        return bad_request_json({"error": AUTHOR_ERROR})
    return req

    
def validate_user_comment(request, comment_id, is_you=True):
    "Validates user and request. Returns json response if error or request"
    if not request.user.is_authenticated():
        return forbidden_json({"error": AUTH_ERROR_TXT})
    try:
        com = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return bad_request_json({"error": "Comment doesn't exist"})
    if is_you and request.user != com.user:
        return bad_request_json({"error": AUTHOR_ERROR})
    return com
