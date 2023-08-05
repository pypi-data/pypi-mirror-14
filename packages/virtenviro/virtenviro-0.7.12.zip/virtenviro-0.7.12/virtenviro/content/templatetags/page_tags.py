# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django import template
from django.db.models import Q
from virtenviro.content.models import Snippet, Page, AdditionalField, Menu
from django.template import loader, Context
from virtenviro.utils import *

register = template.Library()


@register.assignment_tag
def additional_field(page, field_name):
    try:
        additional_field = AdditionalField.objects.get(name=field_name)
        field = page.fieldvalue_set.filter(additional_field=additional_field)
        if field.count() > 0:
            return field[0]
    except AdditionalField.DoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def render_snippet(context, snippet_name):
    try:
        snippet = Snippet.objects.get(name=snippet_name)
    except Snippet.DoesNotExist:
        snippet = None
    if snippet.render:
        t = loader.get_template_from_string(snippet.code)
        res = t.render(Context(context))
        return res

    return snippet.code


@register.simple_tag(takes_context=True)
def render_content(context, content):
    t = loader.get_template_from_string(content)
    return t.render(Context(context))


@register.simple_tag(takes_context=True)
def render_field(context, page, field_name):
    try:
        additional_field = AdditionalField.objects.get(name=field_name)
    except AdditionalField.DoesNotExist:
        return ''
    field = page.fieldvalue_set.filter(additional_field=additional_field)
    if additional_field.render:
        t = loader.get_template_from_string(field.value)
        return t.render(Context(context))
    else:
        return field.value


@register.assignment_tag(takes_context=True)
def get_pages(context, *args, **kwargs):
    parent_id = kwargs.get('parent', 0)
    if parent_id == 0:
        queryset = Page.objects.filter(parent__isnull=True)
    else:
        if isinstance(parent_id, int):
            try:
                parent_node = Page.objects.get(id=parent_id)
            except Page.DoesNotExist:
                return None
        elif isinstance(parent_id, str) or isinstance(parent_id, unicode):
            try:
                parent_node = Page.objects.get(slug=parent_id)
            except Page.DoesNotExist:
                return None
        level = kwargs.get('level', 1) + 1

        queryset = Page.objects.filter(
            level__lte=level,
            tree_id=parent_node.tree_id,
            lft__gte=parent_node.lft,
            rght__lte=parent_node.rght)
        if not kwargs.get('include_parents', False):
            queryset = queryset.exclude(level__lte=parent_node.level)
        if kwargs.get('author', False):
            queryset = queryset.filter(author=kwargs['author'])
    queryset = queryset.order_by(kwargs.get('order', 'id'))
    if context['request'].GET.has_key('page'):
        rpage = context['request'].GET['page']
    else:
        rpage = 1
    if kwargs.get('limit', False):
        queryset = paginate(queryset, rpage, int(kwargs['limit']))
    return queryset


@register.assignment_tag(takes_context=True)
def get_content_ml(context, page, lang):
    content = page.get_content(language=lang)
    return content


@register.assignment_tag
def leaf_pages(root=None, root_id=None, count=0, rnd=False):
    if root is None:
        if root_id is None:
            return []
        else:
            try:
                root = Page.objects.get(pk=root_id)
            except Page.DoesNotExist:
                return []
    nodes = []
    m_nodes = root.get_descendants(include_self=False).order_by('-pub_datetime', '-pk')

    if rnd:
        m_nodes = m_nodes.order_by('?')
    if count == 0:
        count = m_nodes.count()
    for m_node in m_nodes:
        if m_node.is_leaf_node():
            nodes.append(m_node)
        count -= 1
        if count == 0:
            break
    return nodes

@register.assignment_tag
def page_breadcrumb(page):
    breadcrumb = [page]

    while page.parent:
        page = page.parent
        breadcrumb.append(page)
    breadcrumb.reverse()
    return breadcrumb


@register.assignment_tag
def get_page_by_id(page_id):
    try:
        return Page.objects.get(pk=page_id)
    except Page.DoesNotExist:
        return None


@register.assignment_tag
def get_menu(sys_name):
    try:
        menu = Menu.objects.get(sys_name=sys_name)
    except Menu.DoesNotExist:
        return None
    return menu.pagemenurelationship_set.all().order_by('ordering')
