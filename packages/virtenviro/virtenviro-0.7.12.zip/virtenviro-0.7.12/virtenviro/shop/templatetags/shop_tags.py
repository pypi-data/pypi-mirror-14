# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django import template
from django.template import loader, Context
from django.db import  models
from virtenviro.content.models import Snippet, Page, AdditionalField
from virtenviro.shop.models import *
from virtenviro.utils import *
register = template.Library()

'''
@register.assignment_tag(takes_context=True)
def get_content_ml(context, page, lang):
    content = page.get_content(language=lang)
    return content
'''


@register.assignment_tag
def get_product(product_pk):
    try:
        return Product.objects.get(pk=product_pk)
    except Product.DoesNotExist:
        return None

@register.assignment_tag
def get_order(order_pk):
    try:
        return Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return None


@register.assignment_tag
def all_manufacturers():
    return Manufacturer.objects.all()


@register.assignment_tag()
def all_categories(parent=None):
    if parent is None:
        return Category.objects.filter(parent__isnull=True)
    else:
        return Category.objects.filter(parent=parent)


@register.assignment_tag
def random_products(manufacturer=None, count=12):
    products = Product.objects.all()
    if not manufacturer is None:
        products = products.filter(manufacturer=manufacturer)

    return products.order_by('?')[0:count]


@register.assignment_tag
def get_properties_grouped(property_type=None):
    return Property.objects.grouped(property_type=property_type).extra(
        select={
            'intval': 'CAST(substring(value FROM \'^[0-9]+\') AS INTEGER)'},
        order_by=['intval', 'value'])


@register.assignment_tag
def get_property_image(property_value, property_type):
    try:
        pr = Property.objects.filter(value=property_value, property_type=property_type)[0]
        ps = Product.objects.filter(property__value=pr.value, property__property_type=pr.property_type)
        return Image.objects.filter(is_main=True, product__in=ps)[0]
    except:
        return None

@register.assignment_tag
def get_property(product, property_type):
    try:
        return Property.objects.get(product=product, property_type=property_type)
    except Property.DoesNotExist:
        return None

@register.assignment_tag
def most_viewed(count=None):
    if count is None:
        count = getattr(settings, 'SHOP_MOST_VIEWED_COUNT', 10)

    production = Product.objects.all().order_by('-view_count', 'ordering', 'name')[0: count]
    return production

@register.assignment_tag
def discounted(count=None):
    production = Product.objects.filter(discount__gt=0).order_by('?')
    if not count is None:
        production = production[0: count]
    return production


@register.assignment_tag
def get_sellers():
    return Seller.objects.all().order_by('ordering')