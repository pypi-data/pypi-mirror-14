# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
        ('widgetbox', '0009_divider'),
    ]

    operations = [
        migrations.CreateModel(
            name='HTML',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('content', models.TextField(help_text=b'This is unsafe and potentially dangerous. Be aware of what you are doing.')),
            ],
            options={
                'db_table': 'widgetbox_html',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
