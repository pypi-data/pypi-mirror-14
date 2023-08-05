# ~*~ coding: utf-8 ~*~
import os
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from filebrowser.sites import site

urlpatterns = [
    url(r'^filebrowser/', include(site.urls)),
    url(r'^admin/', include('admin.site.urls')),
    url(r'^accounts/', include('virtenviro.registration.urls', namespace='vadmin')),
    url(r'^vadmin/', include('virtenviro.admin.urls', namespace='vadmin'))
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}), ]

urlpatterns += [
    url(r'^', include('virtenviro.content.urls', namespace='vadmin')),
]
