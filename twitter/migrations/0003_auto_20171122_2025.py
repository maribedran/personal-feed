# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 20:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitter', '0002_auto_20171120_0247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'verbose_name': 'Tweet', 'verbose_name_plural': 'Tweets'},
        ),
        migrations.AlterModelOptions(
            name='twitteruser',
            options={'verbose_name': 'Twitter User', 'verbose_name_plural': 'Twitter Users'},
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='twitter_id',
            field=models.BigIntegerField(db_index=True, unique=True, verbose_name='Twitter Id'),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='screen_name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Twitter username'),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='twitter_id',
            field=models.BigIntegerField(db_index=True, unique=True, verbose_name='Twitter Id'),
        ),
        migrations.AlterIndexTogether(
            name='tweet',
            index_together=set([('twitter_id', 'user')]),
        ),
    ]