# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscFields', '0002_auto_20160203_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericfield',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='genericfield',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
