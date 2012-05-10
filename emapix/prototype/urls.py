from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('emapix.prototype.views',
    url(r'^$', 'index'),
)