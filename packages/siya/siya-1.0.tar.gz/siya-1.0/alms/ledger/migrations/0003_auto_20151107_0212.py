# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_auto_20151107_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onedaysentry',
            name='date',
            field=models.DateField(auto_now_add=True, unique=True),
        ),
    ]
