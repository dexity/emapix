from django.conf.urls import patterns, include, url

urlpatterns = patterns('emapix.prototype.views',
                       url(r'^$', 'index'),
                       )
