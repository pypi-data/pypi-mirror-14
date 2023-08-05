# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
        ('widgetbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('question', models.CharField(max_length=400)),
                ('answer', djangocms_text_ckeditor.fields.HTMLField()),
            ],
            options={
                'db_table': 'widgetbox_faqs',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FaqTopic',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=400)),
                ('style', models.CharField(default=b'widgetbox/faqs/default.html', max_length=100, choices=[(b'widgetbox/faqs/default.html', b'Default')])),
            ],
            options={
                'db_table': 'widgetbox_faq_topics',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
