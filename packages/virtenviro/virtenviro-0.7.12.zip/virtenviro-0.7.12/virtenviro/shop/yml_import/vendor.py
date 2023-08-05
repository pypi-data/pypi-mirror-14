#~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'


class Vendor:
    def __init__(self, name, shortTitle=None, slug=None, description=None, logo=None, country=None,
                 city=None, address=None, ordering=None, publish=True):
        """

        :type logo: str
        """
        if logo.startswith('/'):
            logo = logo[1:]

        self.name = name
        self.shortTitle = shortTitle
        self.slug = slug
        self.description = description
        self.logo = logo
        self.country = country
        self.city = city
        self.ordering = ordering
        self.publish = publish
