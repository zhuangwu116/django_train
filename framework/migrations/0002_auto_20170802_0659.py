# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('framework', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editbook',
            name='desc',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
