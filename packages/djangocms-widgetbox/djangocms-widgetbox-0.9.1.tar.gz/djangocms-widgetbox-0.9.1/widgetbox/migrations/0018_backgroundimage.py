# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('filer', '0002_auto_20150606_2003'),
        ('widgetbox', '0017_auto_20160303_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImage',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('extra_css_classes', models.CharField(help_text=b'Use it to add extra CSS classes to background image.', max_length=200, blank=True)),
                ('image', filer.fields.image.FilerImageField(to='filer.Image')),
            ],
            options={
                'db_table': 'widgetbox_background_images',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
