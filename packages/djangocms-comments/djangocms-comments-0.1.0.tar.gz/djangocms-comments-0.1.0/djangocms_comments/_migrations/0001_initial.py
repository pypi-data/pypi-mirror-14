# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import app_data.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('username', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('page_id', models.PositiveIntegerField()),
                ('author_id', models.PositiveIntegerField()),
                ('body', models.TextField()),
                ('requires_attention', models.CharField(max_length=16, choices=[('spam', 'Spam'), ('edited', 'Edited')], blank='')),
                ('moderated', models.CharField(max_length=16, choices=[('spam', 'Spam'), ('edited', 'Edited'), ('deleted', 'Deleted')], blank='')),
                ('moderated_reason', models.CharField(max_length=120, blank=True)),
                ('user_ip', models.GenericIPAddressField()),
                ('user_agent', models.TextField()),
                ('referrer', models.URLField(blank=True)),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
                ('moderated_by', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('page_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(serialize=False, primary_key=True, parent_link=True, related_name='+', to='cms.CMSPlugin')),
                ('published_by_default', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CommentsConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.CharField(verbose_name='type', max_length=100)),
                ('namespace', models.CharField(unique=True, verbose_name='instance namespace', max_length=100, default=None)),
                ('app_data', app_data.fields.AppDataField(editable=False, default='{}')),
            ],
            options={
                'verbose_name': 'config',
                'verbose_name_plural': 'configs',
            },
        ),
        migrations.AddField(
            model_name='comments',
            name='app_config',
            field=models.ForeignKey(to='djangocms_comments.CommentsConfig'),
        ),
    ]
