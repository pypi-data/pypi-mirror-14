# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='/srv/www/virtenviro/../media/img/shop/category', null=True, verbose_name='Image', blank=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='logo',
            field=models.ImageField(upload_to=b'/srv/www/virtenviro/../media/img/shop/manufacturers', null=True, verbose_name='Logo', blank=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='image',
            field=models.ImageField(upload_to=b'/srv/www/virtenviro/../media/img/shop/sellers', null=True, verbose_name='Image', blank=True),
        ),
    ]
