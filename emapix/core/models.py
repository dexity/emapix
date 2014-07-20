from django.db import models
from django.db.transaction import commit_on_success
from django.contrib.auth.models import User

from emapix.utils.const import *
from emapix.utils.utils import timestamp, change_number


class UserProfile(models.Model):
    user        = models.OneToOneField(User)
    location    = models.CharField(max_length=128)
    description = models.CharField(max_length=1000, default="")
    country_alpha2     = models.CharField(max_length=2)
    b_day       = models.SmallIntegerField(null=True, blank=True)
    b_month     = models.CharField(max_length=12, choices=MONTH_CHOICES)   # Full month
    b_year      = models.SmallIntegerField()
    gender      = models.CharField(max_length=1, choices=GENDER_CHOICES)
    activ_token = models.CharField(max_length=64, null=True, blank=True)
    forgot_token = models.CharField(max_length=64, null=True, blank=True)
    num_requests = models.IntegerField(default=0)   # Total requests
    num_photos  = models.IntegerField(default=0)    # Total request photos
    num_comments = models.IntegerField(default=0)   # Total request comments
    
    show_email  = models.BooleanField(default=False)
    show_location   = models.BooleanField(default=True)
    show_birthday   = models.BooleanField(default=False)
    show_gender   = models.BooleanField(default=False)
    
    req_limit   = models.IntegerField(default=10)   # Temp


    def __unicode__(self):
        return "%s, %s" % (self.user, self.location) 


class UserStatus(models.Model):
    user    = models.ForeignKey(UserProfile)
    status  = models.CharField(max_length=16, choices=STATUS_CHOICES)
    updated_date = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        self.updated_date = timestamp()
        super(UserStatus, self).save(*args, **kwargs)        
    
    def __unicode__(self):
        return "%s %s" % (self.user, self.status)


class Photo(models.Model):
    "Photo abstraction"
    user    = models.ForeignKey(User)   # user who uploads the photo
    title   = models.CharField(max_length=64, default="")
    created_time    = models.CharField(max_length=16)  
    updated_time    = models.CharField(max_length=16)
    type    = models.CharField(max_length=16, choices=PHOTO_CHOICES)
    marked_delete   = models.BooleanField(default=False)

    @commit_on_success
    def save(self, *args, **kwargs):
        if not self.id:
            # Photo is just created
            self.created_time = timestamp()     # Updated when object is created
            if self.type == "request":
                change_number(UserProfile, "num_photos", {"user": self.user}, 1)
        self.updated_time = timestamp()
        super(Photo, self).save(*args, **kwargs)
        
    @commit_on_success
    def mark_delete(self):
        if self.type == "request":
            change_number(UserProfile, "num_photos", {"user": self.user}, -1)
        self.marked_delete = True
        self.save()
    
    
    def __unicode__(self):
        # Refactor to "<resource> <type>"
        return "%s %s" % (self.type, self.created_time)


class Image(models.Model):
    "Photo representation"
    photo   = models.ForeignKey(Photo)
    name    = models.CharField(max_length=50, default="")   # unique?
    height  = models.IntegerField(default=0)
    width   = models.IntegerField(default=0)
    url     = models.CharField(max_length=256)   # URL of the photo
    size    = models.IntegerField(default=0)    # Size of image in bytes
    size_type   = models.CharField(max_length=16, choices=IMAGE_SIZES, null=True, blank=True)
    format  = models.CharField(max_length=8, default="")    # jpg, png
    is_avail    = models.BooleanField(default=False)
    created_time    = models.CharField(max_length=16)  
    updated_time    = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_time = timestamp()     # Updated when object is created
        self.updated_time = timestamp()
        super(Image, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name


class Location(models.Model):
    lat     = models.IntegerField(default=0)
    lon     = models.IntegerField(default=0)
    street  = models.CharField(max_length=64, null=True, blank=True)
    city    = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    zipcode = models.CharField(max_length=16, null=True, blank=True)
    res_lat = models.IntegerField(default=0)
    res_lon = models.IntegerField(default=0)
    res_type    = models.CharField(max_length=64, null=True, blank=True)
    
    def __unicode__(self):
        return "(%s, %s)" % (self.lat, self.lon)
    

class Request(models.Model):
    user    = models.ForeignKey(User)           # user who submitted request
    location    = models.ForeignKey(Location)
    description  = models.CharField(max_length=140)
    resource    = models.CharField(max_length=16)       # the photo request identification
    status  = models.CharField(max_length=1, choices=REQ_STATUS_CHOICES, default="o")
    submitted_date  = models.CharField(max_length=16)   # timestamp
    photos  = models.ManyToManyField(Photo, through="PhotoRequest", null=True, blank=True)
    num_comments = models.IntegerField(default=0)

    @commit_on_success
    def save(self, *args, **kwargs):
        if not self.id:
            self.submitted_date = timestamp()
            change_number(UserProfile, "num_requests", {"user": self.user}, 1)
        
        super(Request, self).save(*args, **kwargs)        
    
    @commit_on_success
    def delete(self, *args, **kwargs):
        change_number(UserProfile, "num_requests", {"user": self.user}, -1)
        super(Request, self).delete(*args, **kwargs)
    
    def __unicode__(self):
        return self.resource


class PhotoRequest(models.Model):
    photo       = models.ForeignKey(Photo)
    request     = models.ForeignKey(Request)
    # Some access control (?)
    
    def __unicode__(self):
        return "%s %s" % (self.photo.type, str(self.request))


class ProfilePhoto(models.Model):
    photo       = models.ForeignKey(Photo)
    user        = models.ForeignKey(User)
    
    def __unicode__(self):
        return "%s %s" % (self.photo.type, self.user)


# XXX: Do I need the model?
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
    
    def __unicode__(self):
        return "%s %s" % (str(self.request), self.status)


class Comment(models.Model):
    user    = models.ForeignKey(User)
    text    = models.CharField(max_length=3072, default="")
    submitted_date  = models.CharField(max_length=16)  # timestamp
    
    @commit_on_success
    def save(self, *args, **kwargs):
        if not self.id:
            self.submitted_date = timestamp()
            change_number(UserProfile, "num_comments", {"user": self.user}, 1)

        super(Comment, self).save(*args, **kwargs)
        
    @commit_on_success
    def delete(self, *args, **kwargs):
        change_number(UserProfile, "num_comments", {"user": self.user}, -1)
        super(Comment, self).delete(*args, **kwargs)    
    
    def __unicode__(self):
        return self.text[:20]


class RequestComment(models.Model):
    request = models.ForeignKey(Request)
    comment = models.ForeignKey(Comment)
    
    @commit_on_success
    def save(self, *args, **kwargs):
        "Increment number of comments in request"
        if not self.id:
            change_number(Request, "num_comments", self.request, 1)
        super(RequestComment, self).save(*args, **kwargs)      
    
    @commit_on_success
    def delete(self, *args, **kwargs):
        "Increment number of comments in request"
        change_number(Request, "num_comments", self.request, -1)
        super(RequestComment, self).delete(*args, **kwargs)
        
    def __unicode__(self):
        return "%s %s" % (str(self.request), str(self.comment))
