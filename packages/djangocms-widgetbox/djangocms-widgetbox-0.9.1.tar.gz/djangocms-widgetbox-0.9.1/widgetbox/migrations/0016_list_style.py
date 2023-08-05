# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0015_list_listitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='style',
            field=models.CharField(default=b'', help_text=b'', max_length=100, choices=[(b'widgetbox/list.html', b'default')]),
        ),
    ]
