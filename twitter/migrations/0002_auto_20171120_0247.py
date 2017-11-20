# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='posted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='tweet',
            old_name='content',
            new_name='text',
        ),
        migrations.AddField(
            model_name='tweet',
            name='twitter_id',
            field=models.BigIntegerField(default=1, unique=True, verbose_name='Twitter Id'),
            preserve_default=False,
        ),
    ]
