from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mafia10/', include('mafia10.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^login', 'mafia.views.login'),
    (r'^logout', 'mafia.views.logout'),
    (r'^blog/', include('blog.urls')),
    (r'^joinus/$', 'mafia.views.joinus'),
    (r'^join/$', 'mafia.views.handle_join'),
    (r'^mafiosi/$', 'mafia.views.members_list')
    #(r'^thankyou/$', direct_to_template, {'template': 'thankyou'}),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
