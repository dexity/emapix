from django.contrib import admin
from emapix.core.models import *

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
#admin.site.register(UserStatus)
#admin.site.register(Photo)
#admin.site.register(Image)
#admin.site.register(Location)
#admin.site.register(Request)
#admin.site.register(PhotoRequest)
#admin.site.register(ProfilePhoto)
#admin.site.register(RequestStatus)
#admin.site.register(Comment)
#admin.site.register(RequestComment)


