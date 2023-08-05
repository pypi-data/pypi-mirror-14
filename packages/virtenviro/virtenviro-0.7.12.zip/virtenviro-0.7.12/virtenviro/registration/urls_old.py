# ~*~ coding: utf-8 ~*~
from django.conf.urls import *
import virtenviro.registration.views
import django.contrib.auth.views

urlpatterns = patterns('',
                       url(r'^signup/$', virtenviro.registration.views.signup),
                       url(r'^login/$', django.contrib.auth.views.login,
                           {"template_name": "virtenviro/accounts/login.html"}),
                       url(r'^logout/$', django.contrib.auth.views.logout_then_login, name='logout'),
                       )
