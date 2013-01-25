from django.conf.urls.defaults import patterns, include, url

from emapix.utils.const import USERNAME_REGEX, REQ_REGEX, LOC_REGEX
uregex  = USERNAME_REGEX.lstrip("^").rstrip("$")

urlpatterns = patterns("emapix.core.views",
    url(r"^$", "get_requests"),
    
    # Auth methods
    url(r"^join$", "join"),
    #url(r"^verify$", "verify"),        # Don"t need for now
    #url(r"^verify/resend$", "verify"), # TODO
    url(r"^recaptcha$", "handle_recaptcha"),
    url(r"^confirm/(\w{40})$", "confirm"),
    url(r"^login$", "login"),
    url(r"^logout$", "logout"),
    url(r"^forgot$", "forgot"),
    url(r"^password/renew/(\w{40})$", "renew_password"),
    
    # Request methods
    url(r"^request/make$", "make_request"),
    url(r"^request/%s$" % REQ_REGEX, "get_request"),
    url(r"^requests$", "get_requests"),
    url(r"^requests/%s$" % LOC_REGEX, "get_location_requests"),
    #url(r"^submit/%s$" % REQ_REGEX, "submit"),
    
    # User methods
    url(r"^users$", "users"),
    url(r"^user/(?P<username>(%s))$" % uregex, "get_user"),
    url(r"^user/(?P<username>(%s))/requests$" % uregex, "get_user"),    # XXX: Finish
    url(r"^user/(?P<username>(%s))/photos$" % uregex, "get_user"),      # XXX: Finish
    
    # User profile methods
    url(r"^profile$", "get_profile"),
    url(r"^profile/edit$", "edit_profile"),
    url(r"^profile/password$", "set_password"),
    url(r"^profile/photo$", "get_profile_photo"),
    url(r"^profile/photo/select$", "profile_photo_select"),
    url(r"^profile/photo/crop$", "profile_photo_crop"),
    url(r"^profile/photo/create$", "profile_photo_create"),
    url(r"^profile/photo/remove$", "remove_profile_photo"),
    
    # Photo submit methods
    url(r"^submit/select/%s$" % REQ_REGEX, "submit_select"),
    url(r"^submit/crop/%s$" % REQ_REGEX, "submit_crop"),
    url(r"^submit/create/%s$" % REQ_REGEX, "submit_create"),
    
    # Ajax
    url(r"^request/add$", "add_request"),
    url(r"^request/info/%s$" % REQ_REGEX, "request_info"),
    url(r"^request/%s/edit/json$" % REQ_REGEX, "edit_request_ajax"),
    url(r"^photo/(\d+)/remove/json$", "remove_photo_ajax"),
    url(r"^request/%s/remove/json$" % REQ_REGEX, "remove_request_ajax"),
    url(r"^request/%s/status/(\w+)/json$" % REQ_REGEX, "request_status_ajax"),   # (?P<status>(\w+))
    
    #url(r"^user/(?P<username>(%s))/requests/ajax$" % uregex, "get_user_requests_ajax"),
    #url(r"^user/(?P<username>(%s))/photos/ajax$" % uregex, "get_user_photos_ajax"),
    #url(r"^user/(?P<username>(%s))/areas/ajax$" % uregex, "get_user_areas_ajax"),
    # Json
    url(r"^request/all/json$", "get_requests_json"),
    url(r"^user/(?P<username>(%s))/comments/json$" % uregex, "get_user_comments_json"),
    url(r"^user/(?P<username>(%s))/requests/json$" % uregex, "get_user_requests_json"),
    url(r"^user/(?P<username>(%s))/photos/json$" % uregex, "get_user_photos_json"),
    url(r"^user/(?P<username>(%s))/areas/json$" % uregex, "get_user_areas_json"),   # Not implemented
    url(r"^comments/json$", "get_request_comments_json"),
    url(r"^comment/add/json$", "add_comment_json"),
    url(r"^comment/(\d+)/remove/json$", "remove_comment_json"),
    
    # Layouts
    url(r"^help$", "help"),
    url(r"^photos$", "recent_photos"),
    url(r"^search$", "search"),
    url(r"^search2$", "search2"),
    
    # TODO
    url(r"^about$", "about"),
    url(r"^forum$", "forum"),
    url(r"^feedback$", "feedback"),
    url(r"^developer$", "developer"),
    url(r"^privacy$", "privacy"),
    url(r"^terms$", "terms"),
)