# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationsettings',
            name='current_accession_number',
            field=models.IntegerField(default=b'16414'),
        ),
    ]
