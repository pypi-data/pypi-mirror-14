# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.TextField(default=b'Hami Sabai Ko Library')),
                ('short_name', models.CharField(default=b'HSKL', max_length=100)),
                ('motto', models.TextField(default=b'Reading Is Fun!')),
                ('late_fees_rate', models.IntegerField(default=2)),
                ('max_days_borrow', models.IntegerField(default=10)),
                ('max_books_borrow', models.IntegerField(default=2)),
                ('time_period_report', models.IntegerField(default=3)),
            ],
        ),
    ]
