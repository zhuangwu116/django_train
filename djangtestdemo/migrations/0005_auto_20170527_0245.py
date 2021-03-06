# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangtestdemo', '0004_auto_20170526_0832'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'ordering': ['path']},
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='isvalid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='path_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='types',
            field=models.CharField(default='a', max_length=50),
        ),
    ]
