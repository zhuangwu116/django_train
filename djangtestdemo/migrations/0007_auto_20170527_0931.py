# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangtestdemo', '0006_auto_20170527_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecategory',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
