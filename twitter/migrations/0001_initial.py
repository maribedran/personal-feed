# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 01:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('posted_at', models.DateTimeField(verbose_name='Posted at')),
            ],
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_id', models.BigIntegerField(unique=True, verbose_name='Twitter Id')),
                ('screen_name', models.CharField(max_length=255, unique=True, verbose_name='Twitter username')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitter.TwitterUser', verbose_name='User'),
        ),
    ]