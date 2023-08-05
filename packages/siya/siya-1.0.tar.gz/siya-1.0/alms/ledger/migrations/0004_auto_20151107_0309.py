# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0003_auto_20151107_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onedaysentry',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
