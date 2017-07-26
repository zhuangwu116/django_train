# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import formset_factory
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

ArticleFormSet = formset_factory(ArticleForm,extra=2)
