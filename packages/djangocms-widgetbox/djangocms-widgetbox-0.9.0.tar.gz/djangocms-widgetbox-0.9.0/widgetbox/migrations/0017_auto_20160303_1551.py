# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0016_list_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='tag',
        ),
        migrations.AlterField(
            model_name='list',
            name='style',
            field=models.CharField(default=b'widgetbox/ul.html', help_text=b'Choose list style (template)', max_length=100, choices=[(b'widgetbox/ul.html', b'Unordered list (ul)'), (b'widgetbox/ol.html', b'Ordered list (ol)')]),
        ),
    ]
