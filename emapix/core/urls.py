from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('emapix.core.views',
    url(r'^$', 'requests'),
    
    url(r'^join$', 'join'),
    #url(r'^verify$', 'verify'),        # Don't need for now
    #url(r'^verify/resend$', 'verify'), # TODO
    url(r'^confirm/(\w{40})$', 'confirm'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^password/renew/(\w{40})$', 'renew_password'),
    url(r'^request/make$', 'make_request'),
    url(r'^request/add$', 'add_request'),
    
    # Layouts
    url(r'^forgot$', 'forgot'),
    url(r'^set_profile$', 'set_profile'),
    url(r'^set_password$', 'set_password'),
    url(r'^profile$', 'profile'),
    url(r'^users$', 'users'),
    url(r'^help$', 'help'),
    url(r'^requests$', 'requests'),
    url(r'^request$', 'request'),
    url(r'^request2$', 'request2'),
    url(r'^photos$', 'photos'),
    url(r'^search$', 'search'),
    url(r'^search2$', 'search2'),
    url(r'^submit$', 'submit'),
    url(r'^submit2$', 'submit2'),
    url(r'^submit3$', 'submit3'),
    
)