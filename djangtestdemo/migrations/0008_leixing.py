# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangtestdemo', '0007_auto_20170527_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeiXing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('enable', models.BooleanField(default=False)),
            ],
        ),
    ]
