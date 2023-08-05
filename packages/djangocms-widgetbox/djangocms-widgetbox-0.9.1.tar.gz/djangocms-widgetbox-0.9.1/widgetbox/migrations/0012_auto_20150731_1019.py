# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0011_auto_20150731_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='icon',
            field=models.CharField(help_text=b'Use it for Font Awesome, GLYPHICONS, or similar icons.', max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='button',
            name='link_custom',
            field=models.CharField(help_text=b'Overrides page link if set.', max_length=400, blank=True),
            preserve_default=True,
        ),
    ]
