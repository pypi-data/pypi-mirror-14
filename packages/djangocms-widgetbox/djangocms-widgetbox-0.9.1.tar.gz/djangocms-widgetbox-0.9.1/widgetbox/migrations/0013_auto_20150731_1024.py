# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0012_auto_20150731_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='extra_css_classes',
            field=models.CharField(help_text=b'Use it to add extra CSS classes to button.', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
