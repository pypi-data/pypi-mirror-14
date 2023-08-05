#~*~ coding: utf-8 ~*~
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^import_simple_xml/$', 'virtenviro.shop.views.import_simple_xml', name='import_simple_xml'),
)