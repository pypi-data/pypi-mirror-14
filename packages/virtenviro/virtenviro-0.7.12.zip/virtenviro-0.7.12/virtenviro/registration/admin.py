#~*~ coding: utf-8 ~*~
from django.contrib import admin
from virtenviro.registration.models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'activation_code')

admin.site.register(UserProfile, UserProfileAdmin)