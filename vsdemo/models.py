# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
# Create your models here.
class Poll(models.Model):
    text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    def total_votes(self):
        return self.choice_set.aggregate(Sum('votes'))['votes__sum']
    def ___unicode__(self):
        return self.text
class Choice(models.Model):
    poll=models.ForeignKey(Poll)
    text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
    def votes_percentage(self):
        total=self.poll.total_votes()
        return self.votes/float(total)*100 if total > 0 else 0
    def __unicode__(self):
        return self.text
