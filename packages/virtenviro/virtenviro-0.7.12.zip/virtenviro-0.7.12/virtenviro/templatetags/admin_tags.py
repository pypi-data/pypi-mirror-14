# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.template import Library, loader, Context
from virtenviro.content.models import Page

register = Library()

@register.simple_tag
def page_navigation(current_page=None):
    t = loader.get_template('virtenviro/admin/content/page/navigation.html')
    pages = Page.objects.filter(parent__isnull=True).order_by('title')
    content = t.render(Context({'nodes': pages, 'current_page': current_page}))
    return content


@register.assignment_tag(takes_context=True)
def get_from_dict(context, d, key):
    return d[key]
