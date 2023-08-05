#~*~ coding: utf-8 ~*~
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django import forms
from django.conf import settings
from virtenviro.content.models import *


class TemplateAdmin(admin.ModelAdmin):
    search_fields = ['title', 'filename']


class ContentAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContentAdminForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'ckeditor'

    class Meta:
        model = Content
        fields = [
            'title',
            'h1',
            'intro',
            'content',
            'template',
            'parent',
            'language',

            'meta_title',
            'meta_keywords',
            'meta_description',

            'published',
            'pub_datetime',
            #'last_modified',

            'author',
            # 'last_modified_by',
        ]

        def clean_author(self):
            if not self.cleaned_data['author']:
                return User()
            return self.cleaned_data['author']


class PageAdminForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = [
            'title',
            'slug',
            'is_category',
            'is_home',
            'template',
            'parent',
            'published',
            'pub_datetime',
            'author',
            # 'last_modified_by',
            'login_required',
            'miniature',
        ]

        def clean_author(self):
            if not self.cleaned_data['author']:
                return User()
            return self.cleaned_data['author']


class ContentTabularInline(admin.StackedInline):
    model = Content
    form = ContentAdminForm
    extra = 1


class MenuTabularInline(admin.StackedInline):
    model = PageMenuRelationship
    #form = MenuAdminForm
    extra = 1


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    search_fields = ['title', ]

    form = PageAdminForm
    inlines = [
        ContentTabularInline,
        MenuTabularInline,
    ]

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id

        if db_field.name == 'last_modified_by':
            kwargs['initial'] = request.user.id
        if db_field.name == 'parent':
            kwargs["queryset"] = Page.objects.filter(is_category=True)
        return super(PageAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    class Media:
        try:
            if settings.CKEDITOR:
                js = (
                    '/static/ckeditor/ckeditor.js',
                    '/static/filebrowser/js/FB_CKEditor.js',
                    '/static/js/ckeditor.js',
                )
                css = {'all': ('/static/css/ckeditor.css',), }
        except AttributeError:
            pass


class TagInline(admin.StackedInline):
    model = Tag.content.through
    extra = 3


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'language')
    #list_editable = ('parent',)
    list_filter = ('language',)
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    search_fields = ['title', ]
    inlines = [TagInline,]

    form = ContentAdminForm

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id

        if db_field.name == 'last_modified_by':
            kwargs['initial'] = request.user.id
        return super(ContentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    class Media:
        try:
            if settings.CKEDITOR:
                js = (
                    '/static/ckeditor/ckeditor.js',
                    '/static/filebrowser/js/FB_CKEditor.js',
                    '/static/js/ckeditor.js',
                )
                css = {'all': ('/static/css/ckeditor.css',), }
        except AttributeError:
            pass


class MenuAdmin(admin.ModelAdmin):
    inlines = [
        MenuTabularInline,
    ]


class PageMenuRelationshipAdmin(admin.ModelAdmin):
    list_display = ('pk', 'page', 'title', 'url', 'target', 'code', 'menu_item_type', 'menu', 'ordering')
    list_editable = ('title', 'url', 'target', 'code', 'menu_item_type', 'menu', 'ordering')
    list_filter = ('menu',)

admin.site.register(Page, PageAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(AdditionalField)
admin.site.register(FieldValue)
admin.site.register(Snippet)
admin.site.register(Tag)
admin.site.register(Menu, MenuAdmin)
admin.site.register(PageMenuRelationship, PageMenuRelationshipAdmin)