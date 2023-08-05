# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0006_fix_cms_plugins_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqtopic',
            name='style',
            field=models.CharField(default=b'widgetbox/faq-topic.html', max_length=100, choices=[(b'widgetbox/faq-topic.html', b'default')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gallery',
            name='style',
            field=models.CharField(default=b'widgetbox/gallery.html', max_length=100, choices=[(b'widgetbox/gallery.html', b'default')]),
            preserve_default=True,
        ),
    ]
