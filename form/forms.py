# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

#表单集是同一个页面上多个表单的抽象。它非常类似于一个数据表格。假设有下述表单：
#正如你所看到的，这里仅显示一个空表单。显示的表单的数目通过extra 参数控制。默认情况下，formset_factory() 定义一个表单；下面的示例将显示两个空表单：
ArticleFormSet = formset_factory(ArticleForm)
ArticleFormSetS = formset_factory(ArticleForm,extra=2)

#如果validate_max=True 被提交给 formset_factory(), validation 将在数据集中检查被提交表单的数量,
# 减去被标记删除的, 必须小于等于max_num.
#validate_max=True validates 将会对max_num 严格限制，即使提供的初始数据超过 max_num 而导致其无效
MaxArticleFormSet = formset_factory(ArticleForm,max_num=1,validate_max=True)
#如果validate_min=True被传递到formset_factory()，验证也将检查数据集中的表格数量
# 减去那些被标记为删除的表格数量大于或等于到min_num。
MinArticleFormSet = formset_factory(ArticleForm,min_num=3,validate_min=True)


#自定义表单集验证
class BaseArticleFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        titles = []
        for form in self.forms:
            title = form.cleaned_data['title']
            if title in titles:
                raise forms.ValidationError("Articles in a set must have distinct titles.")
            titles.append(title)
CustomArticleFormSet = formset_factory(ArticleFormSet,formset=BaseArticleFormSet)