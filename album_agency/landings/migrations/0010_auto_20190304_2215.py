# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-04 22:15
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landings', '0009_remove_landingimage_alternative_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staticfile',
            name='static_file',
        ),
        migrations.AddField(
            model_name='staticfile',
            name='static_css',
            field=models.FileField(blank=True, max_length=500, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/landings', location='/Users/dmitrydanilov/Projects/Python/django/album_agency/album_agency/album_agency/landings/static/landings/css'), upload_to='', verbose_name='Static File (.css)'),
        ),
        migrations.AddField(
            model_name='staticfile',
            name='static_font',
            field=models.FileField(blank=True, max_length=500, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/landings', location='/Users/dmitrydanilov/Projects/Python/django/album_agency/album_agency/album_agency/landings/static/landings/fonts'), upload_to='', verbose_name='Static File (fonts)'),
        ),
        migrations.AddField(
            model_name='staticfile',
            name='static_js',
            field=models.FileField(blank=True, max_length=500, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/landings', location='/Users/dmitrydanilov/Projects/Python/django/album_agency/album_agency/album_agency/landings/static/landings/js'), upload_to='', verbose_name='Static File (.js)'),
        ),
    ]
