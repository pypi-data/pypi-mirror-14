# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_unitegallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('theme', models.CharField(default='default', max_length=20, verbose_name='Theme', choices=[('default', 'Default'), ('carousel', 'Carousel'), ('compact', 'Compact'), ('grid', 'Grid'), ('slider', 'Slider'), ('tiles', 'Tiles'), ('tilesgrid', 'Tiles grid')])),
                ('options', models.TextField(help_text='This field allow you to pass a JSON object if you want to customize the gallery. Please consult the Unite gallery docs for a list of options.', verbose_name='Theme options', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=djangocms_unitegallery.models.get_media_path, verbose_name='Photo')),
                ('title', models.CharField(help_text="Leave this blank if you don't want to display a title.", max_length=100, verbose_name='Title', blank=True)),
                ('description', models.CharField(help_text="Leave this blank if you don't want to display a description.", max_length=255, verbose_name='Description', blank=True)),
                ('gallery', models.ForeignKey(related_name='photos', verbose_name='Gallery', to='djangocms_unitegallery.Gallery')),
            ],
        ),
    ]
