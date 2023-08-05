from django.contrib import admin
from django import forms
from django.conf import settings

from virtenviro.news.models import Post, Category


class PostAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'ckeditor'
        self.fields['intro'].widget = forms.Textarea(attrs={'class': 'ckeditor'})

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'slug',
            'intro',
            'content',
            'origin',
            'author',
            'published',
            'pub_datetime',
            'meta_title',
            'meta_keywords',
            'meta_description',
        ]


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'intro', 'content']
    list_filter = ('pub_datetime', )
    form = PostAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id

        if db_field.name == 'last_modified_by':
            kwargs['initial'] = request.user.id
        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    class Media:
        try:
            if settings.CKEDITOR:
                css = {'all': ('/static/css/ckeditor.css',), }
                js = (
                    '/static/ckeditor/ckeditor.js',
                    '/static/filebrowser/js/FB_CKEditor.js',
                    '/static/js/ckeditor.js',
                )
        except AttributeError:
            pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category)