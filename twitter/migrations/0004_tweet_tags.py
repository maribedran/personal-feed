# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 02:55
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_auto_20171122_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None),
        ),
    ]
