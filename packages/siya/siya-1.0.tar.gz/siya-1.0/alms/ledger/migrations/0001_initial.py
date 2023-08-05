# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DrCr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('particulars', models.CharField(max_length=500)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OneDaysEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('drcr_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ledger.DrCr')),
            ],
            bases=('ledger.drcr',),
        ),
        migrations.CreateModel(
            name='Debit',
            fields=[
                ('drcr_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ledger.DrCr')),
            ],
            bases=('ledger.drcr',),
        ),
        migrations.AddField(
            model_name='onedaysentry',
            name='credits',
            field=models.ManyToManyField(default=None, to='ledger.Credit'),
        ),
        migrations.AddField(
            model_name='onedaysentry',
            name='debits',
            field=models.ManyToManyField(default=None, to='ledger.Debit'),
        ),
    ]
