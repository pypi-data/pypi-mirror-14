#~*~ coding: utf-8 ~*~
from django.conf.urls import *
from django.conf import settings
import virtenviro.content.views

SLUG_REGEXP = '[0-9A-Za-z-_.//]+'
if settings.APPEND_SLASH:
    regexp = r'^(?P<slug>%s)/$' % SLUG_REGEXP
else:
    regexp = r'^(?P<slug>%s)/$' % SLUG_REGEXP

urlpatterns = [
    url(r'^$', virtenviro.content.views.home, name='home'),
    url(r'^[a-z0-9-_/]+$', virtenviro.content.views.view, name='page'),
]
