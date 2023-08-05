# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accession_number', models.CharField(max_length=9, db_index=True)),
                ('accessioned_date', models.DateField(auto_now=True, db_index=True)),
                ('call_number', models.CharField(db_index=True, max_length=20, null=True, blank=True)),
                ('title', models.CharField(max_length=255, db_index=True)),
                ('no_of_pages', models.IntegerField(db_index=True)),
                ('language', models.CharField(default=b'EN', max_length=5, db_index=True)),
                ('series', models.CharField(db_index=True, max_length=20, null=True, blank=True)),
                ('edition', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('price', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('volume', models.CharField(db_index=True, max_length=10, null=True, blank=True)),
                ('isbn', models.CharField(max_length=13, null=True, db_index=True)),
                ('state', models.IntegerField(default=0, db_index=True)),
                ('author', models.ManyToManyField(to='head.Author', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookSaver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gifter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_given', models.DateField(auto_now_add=True, db_index=True)),
                ('gifter_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Lend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lending_date', models.DateField(db_index=True)),
                ('returned_date', models.DateField(null=True, db_index=True)),
                ('returned', models.BooleanField(default=False, db_index=True)),
                ('borrowed', models.BooleanField(default=False, db_index=True)),
                ('book', models.ForeignKey(to='head.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('place', models.CharField(max_length=255, db_index=True)),
                ('year', models.CharField(max_length=10, db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='gifted_by',
            field=models.ForeignKey(to='head.Gifter', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='keywords',
            field=models.ManyToManyField(to='head.KeyWord', db_index=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(blank=True, to='head.Publisher', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='saved_by',
            field=models.ManyToManyField(default=django.utils.timezone.now, to='head.BookSaver', db_index=True),
        ),
    ]
