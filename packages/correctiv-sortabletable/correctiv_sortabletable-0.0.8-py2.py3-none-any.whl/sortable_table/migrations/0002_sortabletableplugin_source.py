# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sortable_table', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sortabletableplugin',
            name='source',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
