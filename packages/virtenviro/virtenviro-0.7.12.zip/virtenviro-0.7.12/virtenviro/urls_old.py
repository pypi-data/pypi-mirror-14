#~*~ coding: utf-8 ~*~
import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from filebrowser.sites import site

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'virtenviro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('virtenviro.registration.urls')),
    url(r'^vadmin/', include('virtenviro.admin.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),)

urlpatterns += patterns('',
    url(r'^', include('virtenviro.content.urls')),
)