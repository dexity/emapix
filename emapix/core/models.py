from django.db import models
from django.contrib.auth.models import User
from emapix.utils.const import *

class UserProfile(models.Model):
    user        = models.OneToOneField(User)
    location    = models.CharField(max_length=128)
    country_alpha2     = models.CharField(max_length=2)
    b_day       = models.SmallIntegerField(null=True)
    b_month     = models.CharField(max_length=12)   # Full month
    b_year      = models.SmallIntegerField()
    gender      = models.CharField(max_length=1)
    activ_token = models.CharField(max_length=64, null=True)
    forgot_token = models.CharField(max_length=64, null=True)
    
    req_limit   = models.IntegerField(default=10)   # Temp


class UserStatus(models.Model):
    user    = models.ForeignKey(UserProfile)
    status  = models.CharField(max_length=16, choices=STATUS_CHOICES)
    updated_date = models.CharField(max_length=16)


class Photo(models.Model):
    user    = models.ForeignKey(User)   # user who uploads the photo
    title   = models.CharField(max_length=64, default="")
    source  = models.CharField(max_length=64)   # URL of the photo
    height  = models.IntegerField(default=0)
    width   = models.IntegerField(default=0)
    created_time    = models.CharField(max_length=16)  
    updated_time    = models.CharField(max_length=16)
    
    #picture     # The thumbnail-sized source of the photo
    #images      
    #location


class Location(models.Model):
    lat     = models.IntegerField(default=0)
    lon     = models.IntegerField(default=0)
    street  = models.CharField(max_length=64)
    city    = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    

class Request(models.Model):
    user    = models.ForeignKey(User)  # user who submitted request
    location    = models.ForeignKey(Location)
    #lat     = models.IntegerField(default=0)
    #lon     = models.IntegerField(default=0)
    description  = models.CharField(max_length=140)
    resource    = models.CharField(max_length=16)       # the photo request identification
    submitted_date  = models.CharField(max_length=16)   # timestamp
    photos  = models.ManyToManyField(Photo, through="PhotoRequest", null=True)


class PhotoRequest(models.Model):
    photo       = models.ForeignKey(Photo)
    request     = models.ForeignKey(Request)
    is_avail    = models.BooleanField(default=False)
    # Some access control (?)
    
    def __unicode__(self):
        return ""   #"(%s, %s)" % (self.lat, self.lon)    


class RequestStatus(models.Model):
    request = models.ForeignKey(Request)
    user    = models.ForeignKey(User, null=True)   # user who changes the status
    status  = models.CharField(max_length=1, choices=REQ_STATUS_CHOICES)
    comment = models.CharField(max_length=140, null=True)
    submitted_date  = models.CharField(max_length=16)  # timestamp


#class UserSession(models.Model):
#    pass


"""
Metadata related what user can do and cannot do
"""
