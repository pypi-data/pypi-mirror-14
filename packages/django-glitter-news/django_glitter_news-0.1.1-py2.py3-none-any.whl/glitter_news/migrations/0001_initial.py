# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import glitter.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_assets', '0001_initial'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='LatestNewsBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(null=True, blank=True, to='glitter_news.Category')),
                ('content_block', models.ForeignKey(null=True, editable=False, to='glitter.ContentBlock')),
            ],
            options={
                'verbose_name': 'latest news',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(db_index=True, default=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(unique_for_date='date', max_length=100)),
                ('date', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('date_url', models.DateField(db_index=True, editable=False)),
                ('url', models.URLField(editable=False, blank=True)),
                ('summary', models.TextField(blank=True)),
                ('category', models.ForeignKey(to='glitter_news.Category')),
                ('current_version', models.ForeignKey(null=True, editable=False, to='glitter.Version', blank=True)),
                ('image', glitter.assets.fields.AssetForeignKey(null=True, blank=True, to='glitter_assets.Image')),
            ],
            options={
                'get_latest_by': 'date',
                'default_permissions': ('add', 'change', 'delete', 'edit', 'publish'),
                'abstract': False,
                'ordering': ('-date',),
            },
        ),
    ]
