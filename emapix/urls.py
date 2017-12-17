from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^prototype/', include('emapix.prototype.urls')),
                       #url(r'^layout/', include('emapix.layout.urls')),
                       # url(r'^api/', include('emapix.api.urls')),  # Web service

                       url(r'', include('emapix.core.urls')),

                       # all other requests
                       #(r'^.*', 'emapix.views.forbidden'),

                       url(r'^admin/', include(admin.site.urls)),
                       )
