from django.db import models
from django import forms
from emapix.exceptions import ServiceException


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