# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restructuredText', '0002_homebody_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestructuredText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Name', max_length=255)),
                ('restructuredText', models.TextField(default=b'')),
            ],
        ),
        migrations.DeleteModel(
            name='homeBody',
        ),
    ]
