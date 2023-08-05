# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
        ('widgetbox', '0007_auto_20150522_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='link_custom',
            field=models.CharField(max_length=400, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='link_to_page',
            field=cms.models.fields.PageField(blank=True, to='cms.Page', null=True),
            preserve_default=True,
        ),
    ]
