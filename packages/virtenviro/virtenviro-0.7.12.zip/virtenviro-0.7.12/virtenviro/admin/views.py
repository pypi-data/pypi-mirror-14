# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

template_str = 'virtenviro/admin/%s'


@staff_member_required
def index(request):
    context = {}
    return render(request, template_str % 'index.html', context)


@staff_member_required
def shop(request):

    template = 'virtenviro/admin/shop/home.html'
    context = {
        'appname': 'shop',
    }
    return render(request, template, context)