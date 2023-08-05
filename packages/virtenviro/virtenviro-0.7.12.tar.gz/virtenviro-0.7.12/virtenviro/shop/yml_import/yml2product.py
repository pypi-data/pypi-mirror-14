# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from virtenviro.shop.models import *
from pytils.translit import slugify


class YML2Product:
    def __init__(self, yml):
        self.yml = yml
        self.categories = {}

    def run(self):
        self.add_categories()
        self.add_products()

    def add_categories(self):
        """
        Adds categories
        :return:
        """
        for yml_category in self.yml.categories:
            self.add_category(
                category_id=self.yml.categories.index(yml_category),
                category_name=yml_category['category'],
                parent=yml_category['parentId'])

    def add_category(self, category_id, category_name, parent):
        """

        :param : category_name String
        :param : parent int string or None (parentId)
        :rtype : Category
        """
        if not parent is None:
            yml_parent = self.yml.categories[int(parent)]
            parent = self.add_category(
                category_name=yml_parent['category'],
                parent=yml_parent['parentId'])

        category, created = Category.objects.get_or_create(name=category_name, parent=parent,
                                                           defaults={'slug': slugify(category_name)})
        self.categories[str(category.pk)] = category

        return category

    def add_products(self):
        for offer in self.yml.offers:
            self.add_product(offer)

    def add_product(self, offer):
        """

        :param offer: Offer
        :return: Product
        """
        if not offer.categoryId is None:
            category = self.categories.get(str(offer.categoryId), None)
        else:
            category = None

        discount = 0
        if offer.oldprice:
            price = float(offer.oldprice)
            discount = 1 - (float(offer.price)/price)
        else:
            price = offer.price

        if offer.vendor:
            manufacturer = self.add_manufacturer(offer.vendor)
        else:
            manufacturer = None

        product, created = Product.objects.get_or_create(
            name=offer.name,
            manufacturer=manufacturer,
            defaults={
                'category': category,
                'slug': slugify(offer.name),
                'description': offer.description,
                'price': price,
                'discount': discount,
                'articul': offer.vendorCode,
            })

        for param in offer.params:
            self.add_property(
                value=param['value'],
                property_type=self.add_property_type(name=param['name'], category=category),
                product=product
            )

        for picture in offer.pictures:
            self.add_image(picture, product)

        return product

    def add_manufacturer(self, name):
        """

        :param name: str
        :return: Manufacturer
        """
        manufacturer, created = Manufacturer.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
        return manufacturer

    def add_property(self, value, property_type, product):
        """

        :param value: str or unicode
        :param property_type: PropertyType
        :param product: Product
        :return: Property
        """
        prop, created = Property.objects.get_or_create(
            property_type=property_type,
            product=product,
            value=value
        )
        return prop

    def add_property_type(self, name, category):
        """

        :param name: str
        :param category: Category
        :return: PropertyType
        """
        property_type, created = PropertyType.objects.get_or_create(name=name)
        if created and category:
            ptcr = PropertyTypeCategoryRelation(property_type=property_type, category=category, max_count=1)
            ptcr.save()
        return property_type

    def add_image(self, picture, product):
        """

        :param picture: str image's url
        :param product: Product
        :return:
        """
        if product.manufacturer:
            image_type_str = product.manufacturer.name
        else:
            image_type_str = getattr(settings, 'SHOP_DEFAULT_IMAGE_TYPE', 'Default image type')
        image_type = self.add_image_type(name=image_type_str, category=product.category)
        image, created = Image.objects.get_or_create(
            image=picture,
            product=product,
            defaults={
                'name': product.name,
                'image_type': image_type
            }
        )
        if not product.has_main_image():
            image.is_main = True
            image.save()


    def add_image_type(self, name, category):
        """

        :param name: str or unicode
        :param category: Category
        :return: ImageType
        """
        image_type, created = ImageType.objects.get_or_create(name=name)
        if created and category:
            itcr = ImageTypeCategoryRelation(image_type=image_type, category=category, max_count=1)
            itcr.save()
        return image_type
