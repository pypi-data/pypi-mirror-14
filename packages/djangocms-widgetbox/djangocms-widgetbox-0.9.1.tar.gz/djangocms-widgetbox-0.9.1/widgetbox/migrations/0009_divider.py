# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
        ('widgetbox', '0008_auto_20150710_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='Divider',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('size', models.CharField(max_length=10, choices=[(b'10px', b'10px'), (b'25px', b'25px'), (b'50px', b'50px')])),
            ],
            options={
                'db_table': 'widgetbox_dividers',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
