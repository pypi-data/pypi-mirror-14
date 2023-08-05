#~*~ coding: utf-8 ~*~
from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from virtenviro.shop.models import Product,\
    Category, Property, PropertyType,\
    Image, ImageType, Manufacturer, PropertySlug, PropertyTypeCategoryRelation,\
    ImageTypeCategoryRelation, Currency, File, Seller,\
    OrderStatus, Order, ProductOrderRelation


class APInline(admin.TabularInline):
    model = Property
    extra = 4

    def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
        field = super(APInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        category_id = None
        if request.GET.has_key('category'):
            category_id = request.GET['category']
        else:
            mod = False
            for val in request.path.split('/'):
                try:
                    id = int(val)
                    category_id = Product.objects.get(id = id).category.id
                    mod = True
                    break
                except:
                    pass
        if category_id:
            if db_field.name == 'additional_property_type':
                field.queryset = field.queryset.filter(category=category_id)
        return field
    
class APTInline(admin.TabularInline):
    model = PropertyType.category.through
    extra = 5
    
class ITInline(admin.TabularInline):
    model = ImageType.category.through
    extra = 5


class ImageInline(admin.TabularInline):
    model = Image
    extra = 5

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ImageInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        category_id = None
        if request.GET.has_key('category'):
            category_id = request.GET['category']
        else:
            mod = False
            for val in request.path.split('/'):
                try:
                    id = int(val)
                    category_id = Product.objects.get(id = id).category.id
                    mod = True
                    break
                except:
                    pass
        if category_id and db_field.name == 'image_type':
            field.queryset = field.queryset.filter(category = category_id)
        
        return field


class ProductAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'ckeditor'})

    class Meta:
        model = Product
        exclude = ()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'ordering', 'view_count')
    list_filter = ('category', )
    list_editable = ('price', 'ordering')
    search_fields = ['name', 'category__name', 'slug']
    inlines = [
        APInline,
        ImageInline,
    ]

    form = ProductAdminForm
    valid_lookups = ('parent')


    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        return form

    def lookup_allowed(self, lookup, value):
        if lookup.startswith(self.valid_lookups):
            return True
        
        return super(ProductAdmin, self).lookup_allowed(lookup, value)
        
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

    
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'production_link', 'add_product_link')
    inlines = [APTInline, ITInline]
    
    def add_product_link(self, obj):
        return ('<a href="/admin/shop/product/add/?category=%s" class="addlink">%s</a>' % (obj.id, u'Добавить продукт'))
    add_product_link.allow_tags = True
    
    def production_link(self, obj):
        return ('<a href="/admin/shop/product/?category__id__exact=%s&parent__isnull=True">%s</a>' % (obj.id, u'Продукция'))
    production_link.allow_tags = True


class PropertySlugInline(admin.StackedInline):
    model = PropertySlug
    extra = 0

'''
    if not value_choices is None:
        formfield_overrides = {
            'value': {
                'widget': forms.Select(choices=value_choices)
            }
        }

    def set_value(self, args, kwargs):
        if not self._parent_instance is None:
            self.value_choices = Property.objects.grouped(property_type=self._parent_instance)
'''
#todo: create action to generate slugs for selected property_types properties


class PropertyTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [
        PropertySlugInline,
    ]


class PropertyTypeCategoryRelationAdmin(admin.ModelAdmin):
    list_display = ('property_type', 'category', 'slug', 'max_count')
    list_editable = ('slug', 'max_count')


class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering')
    list_editable = ('ordering',)


class ProductOrderRelationInline(admin.TabularInline):
    model = ProductOrderRelation
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_field', 'created_time', 'modified_time', 'status', 'summary_count', 'summary_products')
    list_filter = ('status', 'created_time', 'modified_time',)

    def summary_count(self, obj):
        return obj.summary_count()
    summary_count.short_description = _('All products count')

    def summary_products(self, obj):
        return obj.summary_products()
    summary_products.short_description = _('Products count')

    def user_field(self, obj):
        return obj.user.email
    user_field.short_description = _('User')

    inlines = [
        ProductOrderRelationInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Property)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Image)
admin.site.register(ImageType)
admin.site.register(Manufacturer)
admin.site.register(PropertySlug)
admin.site.register(PropertyTypeCategoryRelation, PropertyTypeCategoryRelationAdmin)
admin.site.register(ImageTypeCategoryRelation)
admin.site.register(Currency)
admin.site.register(File)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus)
admin.site.register(ProductOrderRelation)