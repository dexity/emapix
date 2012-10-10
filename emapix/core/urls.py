from django.conf.urls.defaults import patterns, include, url

from emapix.utils.const import USERNAME_REGEX, REQ_REGEX
uregex  = USERNAME_REGEX.lstrip("^").rstrip("$")

urlpatterns = patterns('emapix.core.views',
    url(r'^$', 'get_requests'),
    
    url(r'^join$', 'join'),
    #url(r'^verify$', 'verify'),        # Don't need for now
    #url(r'^verify/resend$', 'verify'), # TODO
    url(r'^confirm/(\w{40})$', 'confirm'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^password/renew/(\w{40})$', 'renew_password'),
    url(r'^request/make$', 'make_request'),
    url(r'^request/%s$' % REQ_REGEX, 'get_request'),
    url(r'^requests$', 'get_requests'),
    #url(r'^submit/%s$' % REQ_REGEX, 'submit'),
    url(r'^user/(?P<username>(%s))$' % uregex, 'get_user'),
    url(r'^submit/select/%s$' % REQ_REGEX, 'submit_select'),
    url(r'^submit/crop/%s$' % REQ_REGEX, 'submit_crop'),
    url(r'^submit/create/%s$' % REQ_REGEX, 'submit_create'),
    url(r'^profile/(?P<username>(%s))$' % uregex, 'get_profile'),
    
    # Ajax
    url(r'^request/add$', 'add_request'),
    url(r'^request/info/%s$' % REQ_REGEX, 'request_info'),
    url(r'^request/%s/remove$' % REQ_REGEX, 'remove_request'),
    # Json
    url(r'^request/all/json$', 'get_requests_json'),
    
    # Layouts
    url(r'^forgot$', 'forgot'),
    #url(r'^settings$', 'set_profile'),
    url(r'^set_password$', 'set_password'),
    url(r'^users$', 'users'),
    url(r'^help$', 'help'),
    url(r'^photos$', 'recent_photos'),
    url(r'^search$', 'search'),
    url(r'^search2$', 'search2'),
    
)