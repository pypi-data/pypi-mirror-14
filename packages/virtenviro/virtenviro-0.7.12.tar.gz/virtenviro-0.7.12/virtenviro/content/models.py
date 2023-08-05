# ~*~ coding: utf-8 ~*~
import os
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.conf import settings
from virtenviro.abstract_models import AbstractSeo, AbstractContent, \
    AbstractContentMultilingual
from virtenviro.content.managers import PageManager

LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', 'ru')
LANGUAGES = getattr(settings, 'LANGUAGES', ('ru',))


class Page(MPTTModel):
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.CharField(max_length=250, blank=True, verbose_name=_('Slug'), unique=True)
    is_home = models.BooleanField(default=False, verbose_name=_('Is home page'))
    is_category = models.BooleanField(default=False, verbose_name=_('Is category'))
    template = models.ForeignKey('Template', verbose_name=_('Template'))
    parent = TreeForeignKey('self', blank=True, null=True, related_name='child_set', verbose_name=_('Parent'))

    miniature = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, 'img', 'miniature'),
                                  verbose_name=_('Miniature'), null=True, blank=True)

    # SERVICE FIELDS
    ordering = models.IntegerField(default=999999, verbose_name=_('Ordering'))
    login_required = models.BooleanField(default=False, verbose_name=_('Login required'))
    published = models.BooleanField(default=False, verbose_name=_('Published'))
    pub_datetime = models.DateTimeField(default=timezone.now, verbose_name=_('Created datetime'))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_('Last modified datetime'))

    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='created_pages', blank=True, null=True)
    last_modified_by = models.ForeignKey(User, verbose_name=_('Corrector'), blank=True, null=True,
                                         related_name='modified_pages')

    def get_content(self, language=LANGUAGE_CODE):
        contents = self.contents.filter(language=language)
        if contents:
            return contents[0]
        return None

    def get_contents(self):
        return self.contents.all()

    def get_languages(self):
        languages = []
        for c in self.get_contents():
            languages.append(c.language)
        return languages

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.is_home:
            return '/'
        if self.parent is None:
            return '/%s/' % self.slug
        url = self.get_all_ancestors(self.parent, self.slug)
        return '%s' % url

    get_absolute_url.short_description = _('URL')

    def get_all_ancestors(self, parent, url=''):
        url = '%s/%s' % (parent.slug, url)
        if parent.parent:
            return self.get_all_ancestors(parent.parent, url)
        else:
            return '/%s/' % url

    def clean(self):
        # slugify
        if not self.slug:
            slug = self.title
        else:
            slug = self.slug
        self.slug = slugify(slug)
        if Page.objects.filter(slug=self.slug, parent=None).exclude(id=self.id).exists() and self.parent is None:
            raise ValidationError(
                _('Record with this slug already exists')
            )

    def save(self, *args, **kwargs):
        if self.is_home is True:
            try:
                page = Page.objects.get(is_home=True)
                page.is_home = False
                page.save()
            except Page.DoesNotExist:
                self.is_home = True
        return super(Page, self).save(*args, **kwargs)

    class Meta:
        ordering = ['ordering', '-pub_datetime', 'title']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        unique_together = ('parent', 'slug',)


class Content(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    h1 = models.CharField(max_length=250, verbose_name=_('H1 tag'), null=True, blank=True)
    intro = models.TextField(verbose_name=_('Intro'), null=True, blank=True)
    content = models.TextField(verbose_name=_('Content'), null=True, blank=True)
    template = models.ForeignKey('content.Template', verbose_name=_('Template'), null=True, blank=True)
    language = models.CharField(max_length=10, verbose_name=_('Language'), choices=LANGUAGES, default=LANGUAGE_CODE)

    parent = models.ForeignKey(Page, blank=True, null=True, related_name='contents', verbose_name=_('Parent'))

    # META FIELDS
    meta_title = models.CharField(max_length=250, verbose_name=_('Meta Title'), null=True, blank=True)
    meta_keywords = models.TextField(verbose_name=_('Meta Keywords'), null=True, blank=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), null=True, blank=True)

    # SERVICE FIELDS
    published = models.BooleanField(default=False, verbose_name=_('Published'))
    pub_datetime = models.DateTimeField(default=timezone.now, verbose_name=_('Created datetime'))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_('Last modified datetime'))

    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='created_contents', blank=True, null=True)
    last_modified_by = models.ForeignKey(User, verbose_name=_('Corrector'), blank=True, null=True,
                                         related_name='modified_contents')

    def get_template(self):
        if not self.template is None:
            return self.template
        else:
            return self.parent.template

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.parent.get_absolute_url()

    get_absolute_url.short_description = _('URL')


class Template(MPTTModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'), null=False, blank=False)
    filename = models.CharField(max_length=255, verbose_name=_('Filename'))
    parent = TreeForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)

    def __unicode__(self):
        return '%s [%s]' % (self.title, self.filename)

    class Meta:
        ordering = ['title']
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')


class Snippet(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'), unique=True)
    code = models.TextField(verbose_name=_('Code'), null=True, blank=True)
    render = models.BooleanField(default=False, verbose_name=_('Render'))
    template = models.CharField(max_length=255, verbose_name=_('Template'), null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Snippet')
        verbose_name_plural = _('Snippets')


class AdditionalField(models.Model):
    FIELD_TYPES = (
        ('char', _('Char field')),
        ('text', _('Text field')),
        ('int', _('Integer field')),
        ('float', _('Float field')),
        ('image', _('Image field')),
    )

    name = models.CharField(max_length=255, verbose_name=_('Name'), unique=True)
    field_type = models.CharField(max_length=20, verbose_name=_('Field\'s data type'), choices=FIELD_TYPES)
    template = models.ManyToManyField(Template, verbose_name=_('Templates'), related_name='additional_fields')
    render = models.BooleanField(default=False, verbose_name=_('Render field\'s value'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Additional field')
        verbose_name_plural = _('Additional fields')


class FieldValue(models.Model):
    content = models.ForeignKey(Content, verbose_name=_('Content'))
    additional_field = models.ForeignKey(AdditionalField, verbose_name=_('Additional field'))
    value = models.TextField(verbose_name=_('Value'))

    def __unicode__(self):
        return '%s %s %s' % (self.additional_field.name, _('for'), self.page.title)

    class Meta:
        verbose_name = _('Additional field\'s value')
        verbose_name_plural = _('Additional field\'s values')


class Tag(models.Model):
    tag = models.CharField(max_length=200, verbose_name=_('Tag'))
    content = models.ManyToManyField(Content, verbose_name=_('Content'), related_name='tags')

    def __unicode__(self):
        return self.tag

    class Meta:
        ordering = ['tag', ]
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    sys_name = models.CharField(max_length=255, verbose_name=_('System name'))
    page = models.ManyToManyField(Page, verbose_name=_('Page'), through='PageMenuRelationship')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')


class PageMenuRelationship(models.Model):
    TARGETS = (
        ('_blank', '_blank'),
        ('_self', '_self'),
        ('_parent', '_parent'),
        ('_top', '_top'),
    )

    MENI_ITEM_TYPES = (
        ('page', u'Страница'),
        ('url', u'URL'),
        ('code', u'Код ссылки'),
    )

    page = models.ForeignKey(Page, null=True, blank=True)
    menu = models.ForeignKey(Menu)
    title = models.CharField(max_length=255, verbose_name=_('Title'), null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    target = models.CharField(max_length=15, verbose_name=u'Target', choices=TARGETS, null=True, blank=True)
    code = models.TextField(verbose_name=u'Код ссылки', null=True, blank=True)
    menu_item_type = models.CharField(max_length=25, default=u'page', verbose_name=u'Тип элемента меню',
                                      choices=MENI_ITEM_TYPES)
    ordering = models.IntegerField(default=9999, verbose_name=_('Ordering'))

    def __unicode__(self):
        if self.menu and self.page:
            return '[%s] %s' % (self.menu.name, self.page.title)
        elif self.menu:
            return '[%s] %s' % (self.menu.name, self.pk)
        else:
            return '%s' % self.pk

    class Meta:
        ordering = ['menu', 'ordering']
        verbose_name = _('Page Menu Relationship')
        verbose_name_plural = _('Page Menu Relationships')
