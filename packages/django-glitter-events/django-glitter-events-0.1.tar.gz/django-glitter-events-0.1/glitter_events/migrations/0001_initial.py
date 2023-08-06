# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import glitter.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
        ('glitter_assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('published', models.BooleanField(default=True, db_index=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('location', models.CharField(blank=True, max_length=128)),
                ('summary', models.TextField(help_text='A short sentence description of the event.')),
                ('start', models.DateTimeField(help_text='Start time/date.')),
                ('end', models.DateTimeField(help_text='End time/date.')),
                ('date_url', models.DateField(editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(to='glitter_events.Category')),
                ('current_version', models.ForeignKey(blank=True, to='glitter.Version', editable=False, null=True)),
                ('image', glitter.assets.fields.AssetForeignKey(blank=True, to='glitter_assets.Image', null=True)),
            ],
            options={
                'ordering': ('start',),
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'edit', 'publish'),
            },
        ),
        migrations.CreateModel(
            name='UpcomingEventsBlock',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('category', models.ForeignKey(blank=True, to='glitter_events.Category', null=True)),
                ('content_block', models.ForeignKey(to='glitter.ContentBlock', editable=False, null=True)),
            ],
            options={
                'verbose_name': 'upcoming events',
            },
        ),
    ]
