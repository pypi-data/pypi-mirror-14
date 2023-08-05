# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0003_auto_20150522_0959'),
    ]

    operations = [
        migrations.RenameModel('ButtonPlugin', 'Button'),
        migrations.RenameModel('QuotePlugin', 'Quote'),
        migrations.RenameModel('GalleryPlugin', 'Gallery'),
        migrations.RenameModel('GalleryImagePlugin', 'GalleryImage'),
    ]
