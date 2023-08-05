# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('restructuredText', '0003_auto_20151124_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restructuredtext',
            name='restructuredText',
            field=django_markdown.models.MarkdownField(),
        ),
    ]
