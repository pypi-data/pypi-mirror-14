# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='SortableTablePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('csv_data', models.TextField()),
                ('settings', jsonfield.fields.JSONField(default={}, blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
    ]
