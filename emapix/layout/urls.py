from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('emapix.layout.views',
    url(r'^$', 'index'),
    url(r'^requests$', 'requests'),
)