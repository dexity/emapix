from django.db import models
from django import forms
from emapix.exceptions import ServiceException

class ObjectExists(object):
    
    def __init__(self, message, code, objects=None):
        self.objects    = objects
        self.message    = message
        self.code       = code
    
    def __call__(self, value):
        if not isinstance(self.objects, models.Manager):
            raise ServiceException("Object is invalid")

        items   = self.objects.filter(username = value)
        if len(items) > 0:
            raise forms.ValidationError(self.message, code=self.code)
