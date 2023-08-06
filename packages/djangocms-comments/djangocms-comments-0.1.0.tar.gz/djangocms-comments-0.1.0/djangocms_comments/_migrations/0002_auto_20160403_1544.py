# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentsconfig',
            options={},
        ),
        migrations.RemoveField(
            model_name='commentsconfig',
            name='app_data',
        ),
        migrations.RemoveField(
            model_name='commentsconfig',
            name='namespace',
        ),
        migrations.RemoveField(
            model_name='commentsconfig',
            name='type',
        ),
        migrations.AddField(
            model_name='commentsconfig',
            name='name',
            field=models.CharField(default='Default', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commentsconfig',
            name='open_comments',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='cmsplugin_ptr',
            field=models.OneToOneField(serialize=False, primary_key=True, auto_created=True, to='cms.CMSPlugin', parent_link=True),
        ),
    ]
