# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=200)
    context=models.TextField()
    create_at=models.DateTimeField(default=timezone.now)
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('article-detail',kwargs={'pk':self.pk})