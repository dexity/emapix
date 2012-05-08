from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('api.views',
    url(r'^add$', 'add'),
    url(r'^(?P<reqid>\d+)/remove$', 'remove'),
    url(r'^(?P<reqid>\d+)/update$', 'update'),
    url(r'^(?P<reqid>\d+)$', 'get'),
    url(r'^all$', 'get_all'),
)