# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import ContactForm,ArticleFormSet
import datetime
# Create your views here.
def send_mail(request):
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        if forms.is_valid():
            subject = forms.cleaned_data['subject']
            message = forms.cleaned_data['message']
            sender = forms.cleaned_data['sender']
            cc_myself = forms.cleaned_data['cc_myself']
            recipients = ['562669088@qq.com']
            if cc_myself:
                recipients.append(sender)
            # send_mail(subject,message,sender,recipients)
    else:
        forms = ContactForm()
    return render(request,'form/send_mail.html',{"forms":forms})

def articleformset(request):
    formset = ArticleFormSet(initial=[{
        'title':'django is now open source',
        'pub_date': datetime.date.today(),
    }])
    return render(request,'form/articleformset.html',{"formset":formset})

def formset_validation(request):
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    formset = ArticleFormSet(data)
    print formset.is_valid()

    data.update({
        'form-0-title': 'Test',
        'form-0-pub_date': '1904-16-16',
        'form-1-title': 'Test',
        'form-1-pub_date': '',
    })
    formset = ArticleFormSet(data)
    print formset.is_valid()
    print formset.errors
    print len(formset.errors)
    #想知道表单集内有多少个错误可以使用total_error_count方法
    print formset.total_error_count()
    # ManagementForm¶
    # 你也许已经注意到了那些附加的数据 (form-TOTAL_FORMS, form-INITIAL_FORMS and form-MAX_NUM_FORMS)
    # 他们是必要的，且必须位于表单集数据的最上方 这些必须传递给ManagementForm. ManagementFormThis
    # 用于管理表单集中的表单. 如果你不提供这些数据，将会触发异常
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
        'form-0-title': '',
        'form-0-pub_date': '',
    }
    formset = ArticleFormSet(data)
    #我们也可以检查表单数据是否从初:始值发生了变化 (i.e. the form was sent without any data
    print formset.has_changed()
    #total_form_count返回此表单集中的表单总数
    return render(request,'form/articleformset.html',{'formset':formset})

def customformset_valid(request):
    data = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
        'form-0-title': 'Test',
        'form-0-pub_date': '1904-06-16',
        'form-1-title': 'Test',
        'form-1-pub_date': '1912-06-23',
    }
    formset = ArticleFormSet(data)
    print formset.is_valid()
    print formset.errors
    print formset.non_form_errors()
    return render(request, 'form/articleformset.html', {'formset': formset})
