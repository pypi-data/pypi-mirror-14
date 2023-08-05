# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='page',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='template',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='page',
            name='miniature',
            field=models.ImageField(upload_to=b'/srv/www/virtenviro/../media/img/miniature', null=True, verbose_name='Miniature', blank=True),
        ),
    ]
