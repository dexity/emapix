from django.db import models
from django.db.models import IntegerField, CharField, BooleanField

class PhotoRequest(models.Model):
    lat     = IntegerField(default=0)
    lon     = IntegerField(default=0)
    submitted_date  = CharField(max_length=16)  # timestamp
    resource    = CharField(max_length=16)
    photo_exists    = BooleanField(default=False)
    
    def __unicode__(self):
        return "(%s, %s)" % (self.lat, self.lon)    


#class Request(models.Model):
#    pass
#
#
#class Photo(models.Model):
#    user
#    name
#    picture     # The thumbnail-sized source of the photo
#    source      # The source image of the photo
#    request
#    height
#    width
#    images      
#    location
#    created_time
#    updated_time
#
#
#class PhotoRequest(models.Model):
#    pass
#
#
#class Comment(models.Model):
#    photo   = ""
#    pass
#
#
#class User(models.Model):
#    pass

