# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-03 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import landings.models


class Migration(migrations.Migration):

    dependencies = [
        ('landings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticfile',
            name='static_file',
            field=models.FileField(upload_to=landings.models.get_upload_path, verbose_name='Static Files (.css, .js, fonts)'),
        ),
    ]
