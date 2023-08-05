#~*~ coding: utf-8 ~*~
from mptt.managers import TreeManager

from virtenviro.shop.models import *


class ImageManager(TreeManager):
    def get_one_image(self, product, image_type):
        try:
            image = self.get(product = product, image_type = image_type)
        except Image.DoesNotExist:
            image = None
        return image


class ProductManager(models.Manager):
    def get_product(self, slug):
        try:
            return self.get(slug=slug)
        except Product.DoesNotExist:
            return None
        except Product.MultipleObjectsReturned:
            return None

    def get_product_by_id(self, id):
        try:
            return self.get(id=id)
        except Product.DoesNotExist:
            return None


class PropertyManager(models.Manager):
    def grouped(self, property_type=None):
        if property_type is None:
            return []

        return self.filter(property_type=property_type).values('value').annotate(dcount=models.Count('value'))

    def by_type(self, property_type, product):
        additional_properties = self.filter(property_type=property_type, product=product)

        return additional_properties


class PropertySlugManager(models.Manager):
    def generate(self, property_type):
        # get all properties grouped where property_type = property_type
        properties_grouped = Property.objects.grouped(
            property_type=property_type).extra(
            select={'intval': 'CAST(substring(value FROM \'^[0-9]+\') AS INTEGER)'},
            order_by=['intval', 'value'])

        for property_grouped in properties_grouped:
            # get PropertySlug or create
            property_slug = self.get_or_create(
                value=property_grouped.value,
                property_type=property_type,
                defaults={
                    'slug': set_slug(PropertySlug, property_grouped.value, 60)
                })