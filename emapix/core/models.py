from django.db import models
from django.contrib.auth.models import User
from emapix.utils.const import *

#class User(models.Model):
#    username    = CharField(max_length=32)
#    email       = CharField(max_length=64)
#    name        = CharField(max_length=64)
#    auth        = CharField(max_length=128) # ?
#    gender      = CharField(max_length=1, choices=GENDER_CHOICES)
#    city_state  = CharField(max_length=128)
#    country_alpha2 = CharField(max_length=2, choices=COUNTRY_CHOICES) # ISO 3166:alpha2
#    birthday    = CharField(max_length=8)    # MMDDYYYY
#    created_date    = CharField(max_length=16)  # date when account was first created


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    location    = models.CharField(max_length=128)
    country_alpha2     = models.CharField(max_length=2)
    b_day       = models.SmallIntegerField(blank=True)
    b_month     = models.CharField(max_length=12)   # Full month
    b_year      = models.SmallIntegerField()
    gender      = models.CharField(max_length=1)


class UserStatus(models.Model):
    user    = models.ForeignKey(UserProfile)
    status  = models.CharField(max_length=16, choices=STATUS_CHOICES)
    updated_date = models.CharField(max_length=16)


#class UserSession(models.Model):
#    pass


class PhotoRequest(models.Model):
#    lat     = IntegerField(default=0)
#    lon     = IntegerField(default=0)
#    submitted_date  = CharField(max_length=16)  # timestamp
    resource    = models.CharField(max_length=16)
    photo_exists    = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "(%s, %s)" % (self.lat, self.lon)    


class Request(models.Model):
    user    = models.ForeignKey(User)  # user who submitted request
    lat     = models.IntegerField(default=0)
    lon     = models.IntegerField(default=0)
    submitted_date  = models.CharField(max_length=16)  # timestamp


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

"""
Metadata related what user can do and cannot do
"""
