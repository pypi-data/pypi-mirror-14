# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_comments', '0002_auto_20160403_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='app_config',
            new_name='config',
        ),
    ]
