# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('widgetbox', '0014_auto_20160303_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('tag', models.CharField(default=b'ul', help_text=b'List kind, unordered (&lt;ul&gt;) or ordered (&lt;ol&gt;).', max_length=2, choices=[(b'ul', b'unordered list (<ul>)'), (b'ol', b'ordered list (<ol>)')])),
                ('extra_css_classes', models.CharField(help_text=b'Use it to add extra CSS classes to list.', max_length=200, blank=True)),
            ],
            options={
                'db_table': 'widgetbox_lists',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('item_text', models.CharField(help_text=b'Text value for list item, use it for simple lists.', max_length=400, blank=True)),
                ('extra_css_classes', models.CharField(help_text=b'Use it to add extra CSS classes to list.', max_length=200, blank=True)),
            ],
            options={
                'db_table': 'widgetbox_list_items',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
