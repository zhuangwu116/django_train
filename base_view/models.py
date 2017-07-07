# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=200)
    context=models.TextField()
    create_at=models.DateTimeField(default=timezone.now)
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('article-detail',kwargs={'pk':self.pk})


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def __unicode__(self):
        return self.name

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')
    created_by = models.ForeignKey(User,null=True,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    def __unicode__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    def __str__(self):              # __unicode__ on Python 2
        return self.title
    def __unicode__(self):
        return self.title