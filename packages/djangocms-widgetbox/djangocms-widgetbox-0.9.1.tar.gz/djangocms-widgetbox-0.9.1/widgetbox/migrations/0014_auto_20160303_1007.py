# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('widgetbox', '0013_auto_20150731_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('css_classes', models.CharField(help_text=b'Defines column class, eg col-md-6', max_length=200, blank=True)),
                ('extra_css_classes', models.CharField(help_text=b'Use it to add extra CSS classes to column.', max_length=200, blank=True)),
            ],
            options={
                'db_table': 'widgetbox_columns',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('kind', models.CharField(default=b'container', help_text=b'Container kind, contained or fluid.', max_length=20, choices=[(b'container', b'container'), (b'container-fluid', b'container-fluid')])),
                ('extra_css_classes', models.CharField(help_text=b'Use it to add extra CSS classes to column.', max_length=200, blank=True)),
            ],
            options={
                'db_table': 'widgetbox_containers',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('extra_css_classes', models.CharField(help_text=b'Use it to add extra CSS classes to row.', max_length=200, blank=True)),
            ],
            options={
                'db_table': 'widgetbox_rows',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='divider',
            name='size',
            field=models.CharField(max_length=10),
        ),
    ]
