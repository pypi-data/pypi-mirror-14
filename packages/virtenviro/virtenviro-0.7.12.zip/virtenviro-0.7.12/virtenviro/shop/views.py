#~*~ coding: utf-8 ~*~
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from lxml import etree

from forms import SimpleXmlImportForm
from models import *
from virtenviro.logger import Logger
from virtenviro.utils import id_generator, handle_uploads

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', getattr(settings, 'STATIC_ROOT'))

@login_required
def set_order_status(request, order_id, status_id):
    context = {'res': False, 'errors': []}
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
        try:
            status = OrderStatus.objects.get(pk=status_id)
            order.status = status
            order.save()
            context['res'] = True
        except OrderStatus.DoesNotExist:
            context['errors'].append('Status does not exist')
    except Order.DoesNotExist:
        context['errors'].append('Order does not exist')

    return JsonResponse(context)


@login_required
def import_yml(request):
    from yml_import import YmlParser
    from virtenviro.shop.yml_import.yml2product import YML2Product
    if request.method == 'POST':
        form = SimpleXmlImportForm(request.POST, request.FILES)
        if form.is_valid():
            saved_file = handle_uploads(request, ['xml_file',])['xml_file']
            yml_parser = YmlParser(saved_file)
            yml = yml_parser.parse()
            y2p = YML2Product(yml=yml)
            y2p.run()
    else:
        form = SimpleXmlImportForm()

    return render(request, 'virtenviro/admin/shop/import_yml.html', {'form': form, 'appname': 'shop'})


def import_simple_xml(request):
    if request.method == 'POST':
        form = SimpleXmlImportForm(request.POST, request.FILES)
        if form.is_valid():
            saved_file = handle_uploads(request, ['xml_file',])['xml_file']
            xml_import(init_tree(saved_file))
    else:
        form = SimpleXmlImportForm()

    return render(request, 'virtenviro/shop/xmlimport.html', {'form': form,})


def init_tree(xml_file):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(xml_file, parser)


def xml_import(tree):
    for xml_product in tree.findall('.//product'):
        xml_name = xml_product.find('name').text
        try:
            try:
                xml_category = xml_product.find('category').text
            except:
                xml_category = ''
            try:
                xml_description = xml_product.find('description').text
            except:
                xml_description = ''
            try:
                xml_manufacturer = xml_product.find('manufacturer').text
            except:
                xml_manufacturer = ''
            try:
                xml_articul = xml_product.find('articul').text
            except:
                xml_articul = id_generator(15)
            '''
            unique_code_string = unicode.join(u'', [xml_name, xml_manufacturer, xml_articul])
            unique_code = sha256(unique_code_string)
            '''

            if not xml_manufacturer == '':
                manufacturer, created = Manufacturer.objects.get_or_create(name=xml_manufacturer)
            else:
                manufacturer = None

            if not xml_category == '':
                category, created = Category.objects.get_or_create(name=xml_category, defaults={
                    'parent': None
                })
            else:
                category = None

            product, created = Product.objects.get_or_create(
                name=xml_name,
                manufacturer=manufacturer,
                category=category,
                defaults={
                    'slug': slugify(xml_name),
                    'description': xml_description,
                    'articul': xml_articul
                }
            )
            '''

            product = Product(
                name=xml_name,
                description=xml_description,
                category=category,
                manufacturer=manufacturer,
                articul=xml_articul,
                unique_code=unique_code
            )
            product.save()
            '''

            for xml_image in xml_product.findall('photo'):
                xml_image_attribs = xml_image.attrib
                if xml_image_attribs.get('type', False):
                    image_type, created = ImageType.objects.get_or_create(name=xml_image_attribs['type'])
                else:
                    image_type = None
                if not category is None:
                    image_type_category, created = ImageTypeCategoryRelation.objects.get_or_create(
                        image_type=image_type,
                        category=category,
                        defaults={
                            'max_count': 4
                        }
                    )
                image = Image()
                image.name = product.name
                image.image = '/img/shop/'+xml_image.text
                image.image_type = image_type
                image.product = product
                image.is_main = False if product.has_main_image() else True
                image.save()

            for xml_property in xml_product.findall('property'):
                if xml_property.text:
                    xml_property_attribs = xml_property.attrib
                    property_type, created = PropertyType.objects.get_or_create(
                        name=xml_property_attribs['name'],
                        defaults={
                            'data_type': xml_property_attribs.get('type', -3)
                        }
                    )
                    if category:
                        property_type_category_relation = PropertyTypeCategoryRelation.objects.get_or_create(
                            property_type=property_type,
                            category=category,
                            defaults={
                                'max_count': 1,
                            }
                        )

                    property, created = Property.objects.get_or_create(
                        property_type=property_type,
                        value=xml_property.text,
                        product=product
                    )
        except Exception as inst:
            src = '%s\t|\t can not import' % xml_name
            src = '%s\t|\t%s\t|\t%s' % (src, type(inst), inst.args)
            logger = Logger('import_xml.txt', src)



'''
def create_image(url, title, product, image_type_name = None, download=False):
    try:
        image_type = ImageType.objects.get(name=image_type_name)
    except ImageType.DoesNotExist:
        image_type = ImageType()
        image_type.name = u'Сертификаты'
        image_type.save()
    image = Image()
    image.image_type = image_type
    image_upload_path = os.path.join(settings.STATIC_ROOT, 'files', 'certificate')
    if not os.path.exists(image_upload_path):
        os.makedirs(image_upload_path)
    certificate_file = os.path.join(image_upload_path, '{}.{}'.format(id_generator(12, url.split('.')[-1])))
    if download == True:
        f = open(certificate_file, 'wb')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
        response = opener.open(url)
        data = response.read()
        f.write(data)
        f.close()
    else:
        import shutil
        shutil.copyfile(url, certificate_file)
    image.image = certificate_file
    image.product = product
    image.save()
'''
