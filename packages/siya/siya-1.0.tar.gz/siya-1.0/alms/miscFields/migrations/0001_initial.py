# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=b'What is My name?', max_length=255)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GenericFieldLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(null=True)),
                ('book', models.ForeignKey(to='head.Book')),
            ],
        ),
        migrations.AddField(
            model_name='genericfield',
            name='value',
            field=models.ManyToManyField(to='miscFields.GenericFieldLink'),
        ),
    ]
