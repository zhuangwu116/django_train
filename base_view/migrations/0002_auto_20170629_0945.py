# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base_view', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]