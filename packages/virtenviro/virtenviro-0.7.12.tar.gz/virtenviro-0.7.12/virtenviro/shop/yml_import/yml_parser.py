# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from lxml import etree
from offer import Offer
from yml import YML


def get_text(node, default=None):
        res = default
        try:
            res = node.text
        except AttributeError:
            pass
        except Exception, e:
            print(e.message)
        return res


class YmlParser:

    def __init__(self, yml_file):
        parser = etree.XMLParser(remove_blank_text=True)
        self.yml_tree = etree.parse(yml_file, parser)
        self.yml = YML()

    def parse(self):
        self.parse_categories()
        self.parse_currencies()
        self.parse_shop()
        self.parse_offers()
        return self.yml

    def parse_categories(self):
        categories_tree = self.yml_tree.find('.//categories')
        for category_xml in categories_tree.findall('category'):
            category_name = category_xml.text
            parent_id = category_xml.attrib.get('parentId')
            self.yml.category_append(category=category_name, parent=parent_id)

    def parse_currencies(self):
        currencies_tree = self.yml_tree.find('.//currencies')
        for currency_xml in currencies_tree.findall('currency'):
            currency_attrib = currency_xml.attrib
            if not currency_attrib.get('id', False):
                continue
            self.yml.currency_append(currency_id=currency_attrib.get('id'),
                                     rate=currency_attrib.get('rate', None),
                                     plus=currency_attrib.get('plus', None))

    def parse_shop(self):
        shop_tree = self.yml_tree.find('.//shop')
        self.yml.shop = {
            'name': get_text(shop_tree.find('name')),
            'company': get_text(shop_tree.find('company')),
            'url': get_text(shop_tree.find('url')),
            'platform': get_text(shop_tree.find('platform')),
            'version': get_text(shop_tree.find('version')),
            'agency': get_text(shop_tree.find('agency')),
            'email': get_text(shop_tree.find('email')),
        }
        self.yml.cpa = get_text(shop_tree.find('cpa'))

    def parse_offers(self):
        offer_tree = self.yml_tree.find('.//offers')
        for offer_xml in offer_tree.findall('offer'):
            offer = Offer()
            offer.url = get_text(offer_xml.find('url'))
            offer.price = float(get_text(offer_xml.find('price'), 0.0))
            offer.oldprice = float(get_text(offer_xml.find('oldprice'), 0.0))
            offer.currencyId = get_text(offer_xml.find('currencyId'))
            offer.categoryId = get_text(offer_xml.find('categoryId'))
            for picture in offer_xml.findall('picture'):
                offer.pictures_append(get_text(picture))
            offer.store = get_text(offer_xml.find('store'), 'false')
            offer.pickup = get_text(offer_xml.find('pickup'), 'false')
            offer.delivery = get_text(offer_xml.find('delivery'), 'false')
            offer.local_delivery_cost = get_text(offer_xml.find('local_delivery_cost'))
            offer.name = get_text(offer_xml.find('name'))
            offer.vendor = get_text(offer_xml.find('vendor'))
            offer.vendorCode = get_text(offer_xml.find('vendorCode'))
            offer.description = get_text(offer_xml.find('description'))
            offer.sales_notes = get_text(offer_xml.find('sales_notes'))
            offer.manufacturer_warranty = get_text(offer_xml.find('manufacturer_warranty'))
            offer.country_of_origin = get_text(offer_xml.find('country_of_origin'))
            offer.age = get_text(offer_xml.find('age'))
            if not offer.age is None:
                offer.age_unit = offer_xml.find('age').attrib.get('unit', None)
            offer.barcode = get_text(offer_xml.find('barcode'))
            offer.cpa = get_text(offer_xml.find('cpa'))
            for param_xml in offer_xml.findall('param'):
                try:
                    param_value = get_text(param_xml)
                    param_name = param_xml.attrib.get('name', None)
                    if not param_value is None and not param_name is None:
                        offer.params_append(param_name=param_name, param_value=param_value)
                except AttributeError:
                    pass

            self.yml.offers_append(offer, validate=False)

