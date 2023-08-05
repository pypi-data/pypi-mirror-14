# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0019_tab_tabpane'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabpane',
            name='tabid',
            field=models.SlugField(max_length=200, blank=True),
        ),
    ]
