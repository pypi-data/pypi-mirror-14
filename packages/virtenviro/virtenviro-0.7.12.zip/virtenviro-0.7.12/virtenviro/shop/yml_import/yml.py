# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from category import Category
from vendor import Vendor

class YML:
    def __init__(self):
        self.offers = []
        self.categories = []
        self.vendors = []
        self.shop = {
            'name': None,
            'company': None,
            'url': '',
            'platform': None,
            'version': None,
            'agency': None,
            'email': None,
        }
        self.currencies = []
        self.cpa = None

    def category_append(self, category, description=None, parent=None, slug=None, ordering=99999):
        category = Category(name=category, description=description, slug=slug, ordering=ordering)
        # get parent
        if parent is not None:
            for cat in self.categories:
                if isinstance(parent, int) and cat.id == parent:
                    category.parent = cat
                    break
                elif isinstance(parent, str) and cat.name == parent:
                    category.parent = cat
                else:
                    category.parent = None
        if category not in self.categories:
            self.categories.append(category)

    def currency_append(self, currency_id, rate=None, plus=None):
        """

        :param currency_id:
        :param rate:
        :param plus: %
        :return:
        <currency id="USD" rate="CBRF" plus="1"/> - Курс доллара по ЦБРФ + 1%
        """
        for c in self.currencies:
            if c['id'] == currency_id:
                return

        if rate is None:
            rate = 'CBRF'

        currency = {'id': currency_id, 'rate': rate, 'plus': plus}
        self.currencies.append(currency)

    def offers_append(self, offer, validate=True):
        if validate and offer.validate():
            self.offers.append(offer)
        else:
            self.offers.append(offer)

    def vendor_add(self, name, shortTitle=None, slug=None, description=None, logo=None, country=None,
                   city=None, address=None, ordering=None, publish=True):
        vendor = Vendor(
            name=name,
            shortTitle=shortTitle,
            slug=slug,
            description=description,
            logo=logo,
            country=country,
            city=city,
            address=address,
            ordering=ordering,
            publish=publish)

        if vendor not in self.vendors:
            self.vendors.append(vendor)
