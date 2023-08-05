# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.core.management.base import BaseCommand, CommandError
from lxml import etree

from virtenviro.content.models import Page, AdditionalField, FieldValue, Template


def create_page(title, slug, content, template, is_home=False, intro='',
                parent=None, seo_title=None, seo_keywords=None, seo_description=None):
    """

    :rtype : Page
    """
    try:
        return Page.objects.get(title=title, slug=slug)
    except Page.DoesNotExist:
        page = Page()
        page.title = title
        page.slug = slug
        page.content = content
        page.is_home = is_home
        page.intro = intro
        page.template = template
        page.parent = parent
        page.seo_title = seo_title
        page.seo_keywords = seo_keywords
        page.seo_description = seo_description

        page.save()
        return page


def get_or_create_parent(title, slug, group_template):
    if not title:
        return None

    try:
        parent = Page.objects.get(title=title, slug=slug)
    except Page.DoesNotExist:
        parent = Page()
    parent.title = title
    parent.slug = slug
    parent.is_home = False
    parent.template = group_template
    parent.save()

    return parent


def get_or_create_additional_field(field_name, field_type, render):
    """

    :param field_name: string
    :param field_type: string
    :param render: boolean, string or integer
    :return: AdditionalField
    """

    if isinstance(render, basestring):
        if render == 'False':
            render = False
        else:
            render = True
    else:
        render = bool(render)

    try:
        return AdditionalField.objects.get(name=field_name)
    except AdditionalField.DoesNotExist:
        try:
            render = bool(render)
        except ValueError:
            raise CommandError('Invalid option "render" in file.')
        field = AdditionalField()
        field.name = field_name
        field.field_type = field_type
        field.render = render
        field.save()
        return field


class Command(BaseCommand):
    args = '<xml_file group_template_id page_template_id>'
    help = 'Imports xml file as pages in content application'

    def handle(self, *args, **options):
        if len(args) < 3:
            raise CommandError('Command import_content takes 3 arguments. {} given'.format(len(args)))
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            tree = etree.parse(args[0], parser)
        except IOError:
            raise CommandError('Error reading file \'{0}\': failed to load external entity "{0}"'.format(args[0]))

        try:
            group_template = Template.objects.get(pk=int(args[1]))
        except Template.DoesNotExist:
            raise CommandError('Template {} Does not exist'.format(args[1]))
        except ValueError:
            raise CommandError('Argument 1 is not integer value ')
        try:
            page_template = Template.objects.get(pk=int(args[2]))
        except Template.DoesNotExist:
            raise CommandError('Template {} Does not exist'.format(args[2]))
        except ValueError:
            raise CommandError('Argument 2 is not integer value ')

        for page_xml in tree.iterfind('.//PAGE'):
            title = page_xml.find('TITLE').text
            slug = page_xml.find('SLUG').text
            is_home = False
            intro = page_xml.find('INTRO').text
            content = page_xml.find('CONTENT').text
            template = page_template
            seo_keywords = page_xml.find('SEO_KEYWORDS').text
            seo_description = page_xml.find('SEO_DESCRIPTION').text
            parent_slug = page_xml.find('PARENT_SLUG').text
            parent_title = page_xml.find('PARENT_TITLE').text

            page = create_page(title=title, slug=slug, content=content, template=template, is_home=is_home,
                               intro=intro, parent=get_or_create_parent(title=parent_title, slug=parent_slug,
                                                                        group_template=group_template), seo_title=None,
                               seo_keywords=seo_keywords,
                               seo_description=seo_description)

            for field_xml in page_xml.iterfind('FIELD'):
                field_name = field_xml.find('NAME').text
                field_type = field_xml.find('FIELD_TYPE').text
                field_value = field_xml.find('VALUE').text
                field_render = field_xml.find('RENDER').text

                additional_field = get_or_create_additional_field(field_name, field_type, field_render)
                # todo: if additional field is not in page_template's additional fields list, then add it

                page_field_value = FieldValue()
                page_field_value.page = page
                page_field_value.additional_field = additional_field
                page_field_value.value = field_value
                page_field_value.save()

