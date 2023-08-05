# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('borrow_max_days', models.IntegerField(default=10)),
                ('borrow_max_books', models.IntegerField(default=2)),
                ('late_fees_rate', models.IntegerField(default=2)),
                ('report_time_period', models.IntegerField(default=3)),
                ('org_long_name', models.CharField(default=b'Name Of Your Organization', max_length=1000)),
                ('org_short_name', models.CharField(default=b'Short Name For Your Organization', max_length=500)),
                ('org_motto', models.TextField(default=b'Motto of Your Organization')),
            ],
        ),
    ]
