from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('prototype.views',
    url(r'^$', 'index'),
)