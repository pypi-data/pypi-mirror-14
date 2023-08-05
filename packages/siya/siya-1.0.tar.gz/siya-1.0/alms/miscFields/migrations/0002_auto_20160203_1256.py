# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscFields', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericfield',
            old_name='added_date',
            new_name='date_added',
        ),
    ]
