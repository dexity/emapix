from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('api.views',
    url(r'^(?P<marker_id>\d+)/add$', 'add'),
)