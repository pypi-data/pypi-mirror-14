# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgetbox', '0002_faq_faqtopic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faqtopic',
            old_name='title',
            new_name='topic',
        ),
        migrations.AlterField(
            model_name='faqtopic',
            name='style',
            field=models.CharField(default=b'widgetbox/faq-topic.html', max_length=100, choices=[(b'widgetbox/faq-topic.html', b'Default')]),
            preserve_default=True,
        ),
    ]
