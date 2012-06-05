from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^prototype/', include('emapix.prototype.urls')),
    url(r'^layout/', include('emapix.layout.urls')),
    url(r'^api/', include('emapix.api.urls')),  # Web service

    # all other requests
    #(r'^.*', 'emapix.views.forbidden'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
