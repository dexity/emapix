from django.conf.urls import patterns, include, url

from emapix.utils.const import USERNAME_REGEX, REQ_REGEX, LOC_REGEX
uregex  = USERNAME_REGEX.lstrip("^").rstrip("$")

urlpatterns = patterns("emapix.core.views",
    url(r"^$", "get_requests", name="home"),
    
    # Auth methods
    url(r"^join$", "join", name="join"),
    url(r"^welcome$", "welcome", name="welcome"),   # Redirection after user joined the service
    url(r"^success$", "success", name="login_success"),   # Redirection after successfull form
    url(r"^verify/resend$", "verify_resend", name="verify_resend"),
    url(r"^recaptcha$", "handle_recaptcha", name="recaptcha"),
    url(r"^confirm/(\w{40})$", "confirm", name="registration_confirm"),
    url(r"^login$", "login", name="login"),
    url(r"^logout$", "logout", name="logout"),
    url(r"^forgot$", "forgot", name="forgot_password"),
    url(r"^password/renew/(\w{40})$", "renew_password", name="renew_password"),
    
    # Request methods
    url(r"^request/make$", "make_request", name="make_request"),
    url(r"^request/%s$" % REQ_REGEX, "get_request", name="request"),
    url(r"^requests$", "get_requests", name="requests"),
    #url(r"^requests/%s$" % LOC_REGEX, "get_location_requests"), # Not currently used
    
    # User methods
    url(r"^users$", "users", name="users"),
    url(r"^user/(?P<username>(%s))$" % uregex, "get_user", name="user"),
    url(r"^user/(?P<username>(%s))/(?P<tab>(requests|photos|comments))$" % uregex, "get_user", name="user_section"),
    
    # User profile methods
    url(r"^profile$", "get_profile", name="profile"),
    url(r"^profile/edit$", "edit_profile", name="edit_profile"),
    url(r"^profile/password$", "update_password", name="update_password"),
    url(r"^profile/photo$", "get_profile_photo", name="profile_photo"),
    url(r"^profile/photo/select$", "profile_photo_select", name="profile_photo_select"),
    url(r"^profile/photo/crop$", "profile_photo_crop", name="profile_photo_crop"),
    url(r"^profile/photo/create$", "profile_photo_create", name="profile_photo_create"),
    url(r"^profile/photo/remove/json$", "remove_profile_photo_json", name="remove_profile_photo"),    # XXX: Fix
    
    # Photo methods
    url(r"^submit/select/%s$" % REQ_REGEX, "submit_select", name="submit_select"),
    url(r"^submit/crop/%s$" % REQ_REGEX, "submit_crop", name="submit_crop"),
    url(r"^submit/create/%s$" % REQ_REGEX, "submit_create", name="submit_create"),
    url(r"^photos$", "recent_photos", name="photos"),
    
    # Search methods
    
    # Json
    url(r"^request/all/json$", "get_requests_json", name="get_requests_json"),
    url(r"^request/add$", "add_request", name="add_request"),
    url(r"^request/info/%s$" % REQ_REGEX, "request_info", name="request_info"),
    url(r"^request/%s/edit/json$" % REQ_REGEX, "edit_request_ajax", name="edit_request"),
    url(r"^request/%s/photo/remove/json$" % REQ_REGEX, "remove_request_photo_ajax", name="remove_request_photo"),    # XXX: Fix
    # Note: Is the url pattern r"^request/%s/photo/(\d+)/remove/json$" useful?
    url(r"^request/%s/remove/json$" % REQ_REGEX, "remove_request_ajax", name="remove_request"),
    url(r"^request/%s/status/(\w+)/json$" % REQ_REGEX, "request_status_ajax", name="request_status"),   # (?P<status>(\w+))
    
    url(r"^user/(?P<username>(%s))/comments/json$" % uregex, "get_user_comments_json", name="user_comments"),
    url(r"^user/(?P<username>(%s))/requests/json$" % uregex, "get_user_requests_json", name="user_requests"),
    url(r"^user/(?P<username>(%s))/photos/json$" % uregex, "get_user_photos_json", name="user_photos"),
    url(r"^user/(?P<username>(%s))/areas/json$" % uregex, "get_user_areas_json", name="user_areas"),   # Not implemented
    
    url(r"^comments/json$", "get_request_comments_json", name="request_comments"),
    url(r"^comment/add/json$", "add_comment_json", name="add_comment"),
    url(r"^comment/(\d+)/remove/json$", "remove_comment_json", name="remove_comment"),    # XXX: Fix?
    url(r"^photo/(\d+)/remove/json$", "remove_photo_json", name="remove_photo"), # XXX: Fix
    
    url(r"^status$", "server_status"),

    # Layouts
    url(r"^help$", "help", name="help"),
    url(r"^search$", "search", name="search"),
    url(r"^search2$", "search2", name="search2"),
    
    # TODO
    #url(r"^about$", "about"),
    #url(r"^forum$", "forum"),
    #url(r"^feedback$", "feedback"),
    #url(r"^developer$", "developer"),
    #url(r"^privacy$", "privacy"),
    #url(r"^terms$", "terms"),
)