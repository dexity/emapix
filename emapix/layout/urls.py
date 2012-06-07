from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('emapix.layout.views',
    url(r'^$', 'index'),
    url(r'^requests$', 'requests'),
    url(r'^request$', 'request'),
    url(r'^requests2$', 'requests2'),
    url(r'^photos$', 'photos'),
    url(r'^search$', 'search'),
    url(r'^search2$', 'search2'),
    url(r'^submit$', 'submit'),
    url(r'^submit2$', 'submit2'),
    url(r'^submit3$', 'submit3'),
    url(r'^make$', 'make'),
)