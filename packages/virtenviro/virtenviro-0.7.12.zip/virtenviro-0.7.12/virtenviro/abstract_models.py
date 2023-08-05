# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', 'ru')
LANGUAGES = getattr(settings, 'LANGUAGES', ('ru',))


class AbstractSeo(models.Model):
    # META FIELDS
    meta_title = models.CharField(max_length=250, verbose_name=_('Meta Title'), null=True, blank=True)
    meta_keywords = models.TextField(verbose_name=_('Meta Keywords'), null=True, blank=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), null=True, blank=True)

    class Meta:
        abstract = True


class AbstractContent(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    h1 = models.CharField(max_length=250, verbose_name=_('H1 tag'), null=True, blank=True)
    intro = models.TextField(verbose_name=_('Intro'), null=True, blank=True)
    content = models.TextField(verbose_name=_('Content'), null=True, blank=True)
    template = models.ForeignKey('content.Template', verbose_name=_('Template'), null=True, blank=True)

    def get_template(self):
        if not self.template is None:
            return self.template
        else:
            return self.parent.template

    class Meta:
        abstract = True


class AbstractContentMultilingual(models.Model):
    language = models.CharField(max_length=10, verbose_name=_('Language'), choices=LANGUAGES, default=LANGUAGE_CODE)

    class Meta:
        abstract = True