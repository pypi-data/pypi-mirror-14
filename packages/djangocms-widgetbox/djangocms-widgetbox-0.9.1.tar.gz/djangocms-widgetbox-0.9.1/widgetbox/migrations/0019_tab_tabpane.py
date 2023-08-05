# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('widgetbox', '0018_backgroundimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tab',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('extra_css_classes', models.CharField(help_text=b'Use it to add extra CSS classes to tab.', max_length=200, blank=True)),
            ],
            options={
                'db_table': 'widgetbox_tabs',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TabPane',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200)),
                ('tabid', models.SlugField(max_length=200)),
            ],
            options={
                'db_table': 'widgetbox_tab_panes',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
