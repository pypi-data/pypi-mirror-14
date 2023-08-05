#~*~ coding: utf-8 ~*~

from django.conf.urls import url, include, patterns
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^$', 'virtenviro.admin.views.index', name='home'), )

if 'virtenviro.shop' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url(r'^shop/$', 'virtenviro.admin.views.shop', name='vadmin_shop'),
                            url(r'^shop/import_yml/$', 'virtenviro.shop.views.import_yml',
                                name='vadmin_import_yml'),
                            )
