# -*- coding: utf-8 -*-
from django import forms
from .models import LeiXing
class TestForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(TestForm,self).__init__(*args,**kwargs)
        self.fields['choice_leixing'].widget.choices=LeiXing.objects.all().values_list('id','name')
    c=LeiXing.objects.all().values_list('id','name')
    CHOICES=((True,"是"),(False,"否"))
    choice_leixing=forms.CharField(widget=forms.Select(choices=c))
    choice_enable=forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICES,initial=True)