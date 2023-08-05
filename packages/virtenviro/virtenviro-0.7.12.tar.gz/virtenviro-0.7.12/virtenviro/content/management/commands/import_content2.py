# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django.core.management.base import BaseCommand, CommandError
from lxml import etree

from virtenviro.content.models import Page, Template, Content, Tag


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

        for page_xml in tree.findall('.//page'):
            title = page_xml.find('title').text
            if not title:
                continue
            slug = page_xml.find('slug').text
            try:
                page, created = Page.objects.get_or_create(title=title, slug=slug, is_home=False, template=page_template, published=True)
            except:
                pass

        for page_xml in tree.iterfind('.//page'):
            title = page_xml.find('title').text
            slug = page_xml.find('slug').text
            try:
                page = Page.objects.get(title=title, slug=slug)
            except:
                continue
            try:
                if not title:
                    continue
                content, created = Content.objects.get_or_create(title=title, language='ru',  parent=page,
                                                                 defaults={
                                                                     'published': True,
                                                                     'content': page_xml.find('content').text})
                page_parent_title = page_xml.find('parent').text
                if page_parent_title and not page_parent_title == title:
                    page.parent = Page.objects.filter(title=page_parent_title)[0]
                    page.save()
                    if not page.parent.is_category:
                        pp = page.parent
                        pp.is_category = True
                        pp.template = group_template
                        pp.save()
                tags = page_xml.find('tags')
                for tag_xml in tags.findall('tag'):
                    tag = Tag.objects.get_or_create(tag=tag_xml.text)
                    if not tag in content.tags:
                        content.tags.add(tag)
            except:
                self.stdout.write(u'{} {}'.format(title, slug))

