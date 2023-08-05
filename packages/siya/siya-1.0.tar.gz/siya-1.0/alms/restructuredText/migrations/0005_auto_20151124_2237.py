# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restructuredText', '0004_auto_20151124_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restructuredtext',
            name='restructuredText',
            field=models.TextField(default=b''),
        ),
    ]
