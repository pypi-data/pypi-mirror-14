# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_organizationsettings_current_accession_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrganizationSettings',
        ),
    ]
