from django.db import models
from django.contrib.auth.models import User

from emapix.utils.const import *
from emapix.utils.utils import timestamp


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

    def save(self, *args, **kwargs):
        self.updated_date = timestamp()
        super(UserStatus, self).save(*args, **kwargs)        


class Photo(models.Model):
    "Photo abstraction"
    user    = models.ForeignKey(User)   # user who uploads the photo
    title   = models.CharField(max_length=64, default="")
    created_time    = models.CharField(max_length=16)  
    updated_time    = models.CharField(max_length=16)
    type    = models.CharField(max_length=16, choices=PHOTO_CHOICES)
    marked_delete   = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_time = timestamp()     # Updated when object is created
        self.updated_time = timestamp()
        super(Photo, self).save(*args, **kwargs)


class Image(models.Model):
    "Photo representation"
    photo   = models.ForeignKey(Photo)
    height  = models.IntegerField(default=0)
    width   = models.IntegerField(default=0)
    url     = models.CharField(max_length=64)   # URL of the photo
    size    = models.IntegerField(default=0)    # Size of image in bytes
    size_type   = models.CharField(max_length=16, choices=IMAGE_SIZES)
    is_avail    = models.BooleanField(default=False)


class Location(models.Model):
    lat     = models.IntegerField(default=0)
    lon     = models.IntegerField(default=0)
    street  = models.CharField(max_length=64, null=True)
    city    = models.CharField(max_length=64, null=True)
    country = models.CharField(max_length=64, null=True)
    zipcode = models.CharField(max_length=16, null=True)
    res_lat = models.IntegerField(default=0)
    res_lon = models.IntegerField(default=0)
    res_type    = models.CharField(max_length=64, null=True)
    

class Request(models.Model):
    user    = models.ForeignKey(User)           # user who submitted request
    location    = models.ForeignKey(Location)
    description  = models.CharField(max_length=140)
    resource    = models.CharField(max_length=16)       # the photo request identification
    submitted_date  = models.CharField(max_length=16)   # timestamp
    photos  = models.ManyToManyField(Photo, through="PhotoRequest", null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.submitted_date = timestamp()
        super(Request, self).save(*args, **kwargs)        


class PhotoRequest(models.Model):
    photo       = models.ForeignKey(Photo)
    request     = models.ForeignKey(Request)
    # Some access control (?)
    
    def __unicode__(self):
        return ""


class RequestStatus(models.Model):
    request = models.ForeignKey(Request)
    user    = models.ForeignKey(User, null=True)   # user who changes the status
    status  = models.CharField(max_length=1, choices=REQ_STATUS_CHOICES)
    comment = models.CharField(max_length=140, null=True)
    submitted_date  = models.CharField(max_length=16)  # timestamp

    def save(self, *args, **kwargs):
        if not self.id:
            self.submitted_date = timestamp()
        super(RequestStatus, self).save(*args, **kwargs)        

"""
Metadata related what user can do and cannot do
"""
