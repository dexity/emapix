from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^prototype/', include('emapix.prototype.urls')),
    #url(r'^layout/', include('emapix.layout.urls')),
    #url(r'^api/', include('emapix.api.urls')),  # Web service

    url(r'', include('emapix.core.urls')),
    
    # all other requests
    #(r'^.*', 'emapix.views.forbidden'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
