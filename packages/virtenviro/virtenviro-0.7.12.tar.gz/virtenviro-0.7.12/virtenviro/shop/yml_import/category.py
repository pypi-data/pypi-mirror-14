# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'


class Category:
    def __init__(self, name, description=None, parent=None, slug=None, ordering=99999):
        self.id = 0
        self.name = name
        self.description = description
        self.slug = slug
        self.ordering = ordering
        self.parent = parent

