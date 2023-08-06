# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_comments', '0003_auto_20160403_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='config',
            field=models.ForeignKey(to='djangocms_comments.CommentsConfig', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commentsconfig',
            name='akismet',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='commentsconfig',
            name='published_by_default',
            field=models.BooleanField(default=True),
        ),
    ]
