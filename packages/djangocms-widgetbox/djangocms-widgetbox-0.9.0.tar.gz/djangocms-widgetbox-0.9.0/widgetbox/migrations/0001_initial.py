# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangocms_text_ckeditor.fields
import filer.fields.image
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
        ('filer', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ButtonPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=200, blank=True)),
                ('link_custom', models.CharField(max_length=400, blank=True)),
                ('icon', models.CharField(max_length=50, blank=True)),
                ('link_to_page', cms.models.fields.PageField(blank=True, to='cms.Page', null=True)),
            ],
            options={
                'db_table': 'widgetbox_buttons',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GalleryImagePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=100, blank=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('image', filer.fields.image.FilerImageField(to='filer.Image')),
            ],
            options={
                'db_table': 'widgetbox_gallery_images',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GalleryPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('style', models.CharField(default=b'default', max_length=100, choices=[(b'default', b'default')])),
            ],
            options={
                'db_table': 'widgetbox_galleries',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='QuotePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('content', djangocms_text_ckeditor.fields.HTMLField()),
                ('name', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=400, blank=True)),
                ('image', filer.fields.image.FilerImageField(blank=True, to='filer.Image', null=True)),
            ],
            options={
                'db_table': 'widgetbox_quotes',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
