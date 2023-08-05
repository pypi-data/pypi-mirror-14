#~*~ coding: utf-8 ~*~
import os
import string
from django.conf import settings
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pytils.translit import slugify
import random
from virtenviro.shop.models import *

UPLOAD_PATH = getattr(settings, 'UPLOAD_PATH', 'upload')


def set_slug(model, src, length=60):
    slug = slugify(src)[0:length]
    try:
        obj = model.objects.get(slug=slug)
        slug = set_slug(model, slug, length)
    except model.DoesNotExist:
        return slug


def set_main_images():
    production = Product.objects.all()
    for product in production:
        if product.has_main_image():
            pass
        else:
            images = product.image_set.all()
            if images:
                image = images[0]
                image.is_main = True
                image.save()
            else:
                try:
                    print 'Product %s [%s] has no image' % (product.title, product.pk)
                except:
                    print 'Product RUS [%s] has no image' % (product.pk)


def set_any_image():
    production = Product.objects.all()
    i = 0
    for product in production:
        if not product.image_set.all():
            if not product.is_leaf_node():
                children = product.get_children()
                for child in children:
                    if child.has_main_image():
                        cimage = child.get_main_image()
                        image = Image()
                        image.image = cimage.image
                        image.title = product.title
                        image.product = product
                        image.image_type = cimage.image_type
                        image.is_main = True
                        image.save()
                        i = i + 1
                        break
    print 'I\'ve set %s images' % i


def ucode(str, encoding="utf-8", errors="ignore"):
    return unicode(str, encoding=encoding, errors=errors)


def handle_uploads(request, keys):
    saved = {}
    upload_full_path = os.path.join(settings.STATIC_ROOT, 'upload')

    # check and make upload_full_path
    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    # read request.FILES and write files
    for key in keys:
        if key in request.FILES:
            upload = request.FILES[key]
            while os.path.exists(os.path.join(upload_full_path, upload.name)):
                upload.name = '_' + upload.name
            dest = open(os.path.join(upload_full_path, upload.name), 'wb')
            for chunk in upload.chunks():
                dest.write(chunk)
            dest.close()
            saved[key] = os.path.join(upload_full_path, upload.name)
    # returns {key1: path1, key2: path2, ...}
    return saved


def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def paginate(objects, page=1, count=10):
    paginator = Paginator(objects, count)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return pages


def sha256(str):
    import hashlib
    m = hashlib.sha256()
    m.update(str)
    return m.digest()


'''
from importlib import import_module
module_ = import_module('path.to.module')
module_.call_some_method()
module_.variable
'''
