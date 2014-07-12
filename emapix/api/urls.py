from django.conf.urls import patterns, include, url

urlpatterns = patterns('emapix.api.views',
    url(r'^add$', 'add'),
    url(r'^upload$', 'upload'),
    url(r'^(?P<reqid>\d+)/remove$', 'remove'),
    url(r'^(?P<reqid>\d+)/update$', 'update'),
    url(r'^(?P<reqid>\d+)$', 'get'),
    url(r'^all$', 'get_all'),
)