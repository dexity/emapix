from django.contrib import admin
from emapix.core.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display    = ("user", "location","country_alpha2", "description", "gender",
                       "activ_token", "num_requests", "num_photos", "num_comments")

class UserStatusAdmin(admin.ModelAdmin):
    list_display    = ("user", "status", "updated_date")

class PhotoAdmin(admin.ModelAdmin):
    list_display    = ("user", "created_time", "updated_time", "type", "marked_delete")

class ImageAdmin(admin.ModelAdmin):
    list_display    = ("photo", "name", "height", "width", "url", "size", "size_type",
                       "format")

class LocationAdmin(admin.ModelAdmin):
    list_display    = ("lat", "lon", "street", "city", "country", "zipcode",
                       "res_lat", "res_lon", "res_type")

class RequestAdmin(admin.ModelAdmin):
    list_display    = ("user", "location", "description", "resource", "status",
                       "submitted_date", "num_comments")

class PhotoRequestAdmin(admin.ModelAdmin):
    list_display    = ("photo", "request")

class ProfilePhotoAdmin(admin.ModelAdmin):
    list_display    = ("photo", "user")

class RequestStatusAdmin(admin.ModelAdmin):
    list_display    = ("request", "user", "status")
 
class CommentAdmin(admin.ModelAdmin):
    list_display    = ("user", "text", "submitted_date")

class RequestCommentAdmin(admin.ModelAdmin):
    list_display    = ("request", "comment")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserStatus, UserStatusAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(PhotoRequest, PhotoRequestAdmin)
admin.site.register(ProfilePhoto, ProfilePhotoAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(RequestComment, RequestCommentAdmin)


