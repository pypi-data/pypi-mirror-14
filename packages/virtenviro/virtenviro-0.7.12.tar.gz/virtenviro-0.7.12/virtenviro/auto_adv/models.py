# ~*~ coding: utf-8 ~*~
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import slugify
from django.conf import settings
from virtenviro.utils import set_slug, sha256, id_generator
from managers import *

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', getattr(settings, 'STATIC_ROOT'))


class Mark(MPTTModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.CharField(max_length=60, verbose_name=_('Slug'), null=True, blank=True)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), related_name='subcategories', null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    image = models.ImageField(upload_to=_(os.path.join(MEDIA_ROOT, 'img', 'auto_adv', 'category')), verbose_name=_('Image'), null=True, blank=True)

    # SERVICE FIELDS
    view_count = models.IntegerField(default=0, verbose_name=_('Count of views'), blank=True, null=True)

    # META FIELDS
    meta_title = models.CharField(max_length=250, verbose_name=_('Meta Title'), null=True, blank=True)
    meta_keywords = models.TextField(verbose_name=_('Meta Keywords'), null=True, blank=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), null=True, blank=True)

    def __unicode__(self):
        return self.name

    def clean(self):
        if not self.slug:
            self.slug = set_slug(Mark, self.name, length=60)

    def get_absolute_url(self):
        if self.parent is None:
            return '/%s/' % self.slug
        else:
            url = self.get_all_ancestors(self.parent, self.slug)
        return '%s' % url

    get_absolute_url.short_description = _('URL')

    def get_all_ancestors(self, parent, url=''):
        url = '%s/%s' % (parent.slug, url)
        if parent.parent:
            return self.get_all_ancestors(parent.parent, url)
        else:
            return '/%s/' % url

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Model(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.CharField(max_length=60, verbose_name=_('Slug'), null=True, blank=True)
    mark = models.ForeignKey(Mark, verbose_name=_('Mark'), related_name='children', null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)

    # SERVICE FIELDS
    view_count = models.IntegerField(default=0, verbose_name=_('Count of views'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    def new_price(self):
        discount = self.discount/100
        price = self.price - self.price * discount
        return price

    def clean(self, *args, **kwargs):
        if not self.slug:
            self.slug = set_slug(Model, self.name, length=60)

        if not self.articul:
            self.articul = id_generator(size=15)
        '''
        if not self.unique_code:
            if self.manufacturer:
                manufacturer = self.manufacturer.name
            else:
                manufacturer = ''
            unique_code_string = '{}{}{}'.format(self.name, manufacturer, self.articul)
            self.unique_code = sha256(unique_code_string)
        '''

    def get_main_images(self):
        return self.image_set.all().filter(is_main=True)

    def get_main_image(self):
        main_images = self.image_set.all().filter(is_main=True)
        if not main_images:
            return None
        else:
            return main_images[0]

    def has_main_image(self):
        if self.image_set.all().filter(is_main=True):
            return True
        else:
            return False
        return False

    def filter_group(self):
        return self.filter(is_group=True)

    def filter_parent_group(self):
        return self.filter(is_group=True, parent__isnull=True)

    def get_absolute_url(self):
        return '%s%s/' % (self.category.get_absolute_url(), self.slug)

    get_absolute_url.short_description = _('URL')

    class Meta:
        ordering = ['name']
        verbose_name = _('Model')
        verbose_name_plural = _('Models')


class Advert(models.Model):
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    price = models.FloatField(verbose_name=_('Price'), default=0.0)
    contacts = models.TextField(verbose_name=_('Contacts'), null=True, blank=True)
    created_datetime = models.DateTimeField(verbose_name=_('Creation datetime'))
    model = models.ForeignKey(Model, verbose_name=_('Model'))
    archive = models.BooleanField(default=False, verbose_name=_('In archive'))
    sold = models.BooleanField(default=False, verbose_name=_('Sold'))
    change_datetime = models.DateTimeField(verbose_name=_('Changing datetime'))
    user = models.ForeignKey(User, verbose_name=_('User'))

    # SERVICE FIELDS
    view_count = models.IntegerField(default=0, verbose_name=_('Count of views'), blank=True, null=True)
    identifier = models.CharField(max_length=255, verbose_name=_('Identifier for importing'))

    objects = AdvertManager()

    def get_absolute_url(self):
        return '%s%s/' % (self.model.get_absolute_url(), self.pk)

    class Meta:
        ordering = ['-created_datetime', '-change_datetime']
        verbose_name = _('Model')
        verbose_name_plural = _('Models')


class PropertyType(models.Model):
    DATA_TYPES = (
        (-1, _('Integer'),),
        (-2, _('Float')),
        (-3, _('String')),
        (-4, _('Text')),
        (-5, _('Boolean')),
        (-6, _('Html')),
    )
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    data_type = models.IntegerField(verbose_name=_('Data type'), default=-1, choices=DATA_TYPES)

    def __unicode__(self):
        return '%s [%s]' % (self.name, self.pk)

    class Meta:
        ordering = ['name']
        verbose_name = _('Properties type')
        verbose_name_plural = _('Properties Types')


class Property(models.Model):
    property_type = models.ForeignKey(PropertyType)
    value = models.TextField(verbose_name=_('Value'))
    advert = models.ForeignKey(Advert, verbose_name=_('Advert'))

    objects = PropertyManager()

    def __unicode__(self):
        return '%s: %s' % (self.property_type.name, self.value)

    class Meta:
        ordering = ['property_type__name', 'value']
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')


class Image(models.Model):
    image = FileBrowseField("Image", max_length=200, directory=os.path.join(MEDIA_ROOT, 'img', 'auto_adv'),
                            blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'), blank=True, null=True)
    advert = models.ForeignKey(Advert, verbose_name=_('Advert'))
    is_main = models.BooleanField(default=False, verbose_name=_('Is Main'))

    def __unicode__(self):
        return '%s [%s%s]' % (self.name, MEDIA_ROOT, self.image)

    class Meta:
        ordering = ['image_type', 'name']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')