# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class EditBook(models.Model):
    name = models.CharField(null=True,blank=True,max_length=100)
    desc = models.TextField(null=True,blank=True,max_length=5000)


