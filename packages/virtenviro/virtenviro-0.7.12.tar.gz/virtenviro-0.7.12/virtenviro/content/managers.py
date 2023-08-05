# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.db import models
import datetime


class PageManager(models.Manager):
    def get_pages(self, parent=None, order=['ordering', '-pub_datetime', 'title'], author=None):
        pages = self.filter(published=True, pub_datetime__lte=datetime.datetime.now())
        if not parent is None:
            pages = pages.filter(
                level__lte=parent.level,
                tree_id=parent.tree_id,
                lft__gte=parent.lft,
                rght__lte=parent.rght)
        if not author is None:
            pages = pages.filter(author=author)
        return pages.order_by(*order)
