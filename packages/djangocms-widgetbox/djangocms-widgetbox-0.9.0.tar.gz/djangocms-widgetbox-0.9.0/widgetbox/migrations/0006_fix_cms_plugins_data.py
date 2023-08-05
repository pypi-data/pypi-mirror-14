# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_cms_plugins(apps, schema_editor):
    CMSPlugin = apps.get_model('cms', 'CMSPlugin')
    CMSPlugin.objects.filter(plugin_type="CMSButtonPlugin").update(plugin_type="ButtonPlugin")
    CMSPlugin.objects.filter(plugin_type="CMSQuotePlugin").update(plugin_type="QuotePlugin")
    CMSPlugin.objects.filter(plugin_type="CMSGalleryPlugin").update(plugin_type="GalleryPlugin")
    CMSPlugin.objects.filter(plugin_type="CMSGalleryImagePlugin").update(plugin_type="GalleryImagePlugin")


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0005_rename_model_button'),
    ]

    operations = [
        migrations.RunPython(fix_cms_plugins)
    ]
