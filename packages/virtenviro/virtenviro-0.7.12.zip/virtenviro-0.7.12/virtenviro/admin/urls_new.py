# ~*~ coding: utf-8 ~*~

from django.conf.urls import url, include
from django.conf import settings
import virtenviro.admin.views

app_name = 'vadmin'

urlpatterns = [
    url(r'^$', virtenviro.admin.views.index, name='home'),
]

if 'virtenviro.content' in settings.INSTALLED_APPS:
    import virtenviro.content.admin_views

    urlpatterns += [
        url(r'^content/page/$', virtenviro.content.admin_views.content_page, name='content_page'),
        url(r'^content/page/(?P<page_id>\d+)/$', virtenviro.content.admin_views.content_page_edit,
            name='content_page_edit'),
        url(r'^content/page/add/$', virtenviro.content.admin_views.content_page_add, name='content_page_add'),
        url(r'^content/template/$', virtenviro.content.admin_views.content_template, name='content_template'),
        url(r'^content/template/(?P<template_id>\d+)/$', virtenviro.content.admin_views.content_template_form,
            name='content_template_edit'),
        url(r'^content/template/add/$', virtenviro.content.admin_views.content_template_form,
            name='content_template_add'),
    ]

if 'virtenviro.shop' in settings.INSTALLED_APPS:
    import virtenviro.admin.views
    import virtenviro.shop.views

    urlpatterns += [
        url(r'^shop/$', virtenviro.admin.views.shop, name='vadmin_shop'),
        url(r'^shop/import_yml/$', virtenviro.shop.views.import_yml, name='vadmin_import_yml'),
    ]
