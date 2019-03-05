# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-02 21:56
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import landings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Landing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('title_page', models.CharField(default='', max_length=250, verbose_name='Title for page')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta description')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is landing active?')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='Date changed')),
            ],
            options={
                'verbose_name': 'Landing',
                'verbose_name_plural': 'Landings',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='LandingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=landings.models.upload_path, verbose_name='Cover picture')),
                ('alternative_text', models.CharField(max_length=250, verbose_name='Alternative Image Text')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('landing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landings.Landing', verbose_name='Landing Page')),
            ],
            options={
                'verbose_name': 'Landing Image',
                'verbose_name_plural': 'Landing Images',
            },
        ),
        migrations.CreateModel(
            name='StaticFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('static_file', models.FileField(storage=landings.models.get_upload_path, upload_to='', verbose_name='Static Files (.css, .js, fonts)')),
                ('file_type', models.SmallIntegerField(choices=[(0, 'CSS File'), (1, 'Font'), (2, 'JavaScript File')], verbose_name='File Type')),
                ('is_active', models.BooleanField(verbose_name='Is Active?')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Static File',
                'verbose_name_plural': 'Static Files',
            },
        ),
        migrations.CreateModel(
            name='TemplateFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Same object name as for uploaded file', max_length=250, verbose_name='Name')),
                ('template_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url='/landings', location='/Users/dmitrydanilov/Projects/Python/django/album_agency/album_agency/landings/templates/landings'), upload_to='', verbose_name='Template file (HTML file)')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is template active?')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Template File',
                'verbose_name_plural': 'Template Files',
            },
        ),
        migrations.AddField(
            model_name='landing',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='landings.TemplateFile', verbose_name='Template'),
        ),
    ]
