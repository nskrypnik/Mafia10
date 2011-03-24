from django.conf.urls.defaults import *
from django.conf import settings
from tagging.views import tagged_object_list
from models import Entry
 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
 
urlpatterns = patterns('',
    # Example:
    # (r'^simcms/', include('simcms.foo.urls')),
 
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
 
    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
 
    (r'^$', 'blog.views.entries_index'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'blog.views.entry_detail'),
    (r'^bytag/(?P<tag>.*)/$', 'blog.views.entry_bytag'),
    (r'^resize/(?P<width>\d{1,4})/(?P<height>\d{1,4})/(?P<path>.*)/$', 'blog.views.resize'),
)
 
#if settings.DEBUG:
if False:
    # http://docs.djangoproject.com/en/1.0/howto/static-files/
    # http://docs.djangoproject.com/en/1.0/howto/deployment/modpython/#serving-media-files
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),    # development
        #(r'^index.py/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),    # production
    )

