from django.db import models
from django.db.models import IntegerField, CharField

class PhotoRequest(models.Model):
    lat     = IntegerField(default=0)
    lon     = IntegerField(default=0)
    submitted_date  = CharField(max_length=16)  # timestamp
    resource    = CharField(max_length=16)
    
    def __unicode__(self):
        return "(%s, %s)" % (self.lat, self.lon)    
