# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0010_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='extra_css_classes',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
