# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.forms.formsets import formset_factory
from forms import ContactForm,ArticleFormSet,\
    CustomArticleFormSet,MaxArticleFormSet,\
    MinArticleFormSet,ArticleForm,AddArticleFormSet
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
    formset = CustomArticleFormSet(data)
    print formset.is_valid()
    print formset.errors
    print formset.non_form_errors()
    return render(request, 'form/articleformset.html', {'formset': formset})
def formset_validate_max(request):
    data = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '',
        'form-MAX_NUM_FORMS': '',
        'form-0-title': 'Test',
        'form-0-pub_date': '1904-06-16',
        'form-1-title': 'Test',
        'form-1-pub_date': '1912-06-23',
    }
    formset = MaxArticleFormSet(data)
    print formset.is_valid()
    print formset.errors
    print formset.non_form_errors()
    return render(request, 'form/articleformset.html', {'formset': formset})
def formset_validate_min(request):
    data = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '',
        'form-MAX_NUM_FORMS': '',
        'form-0-title': 'Test',
        'form-0-pub_date': '1904-06-16',
        'form-1-title': 'Test',
        'form-1-pub_date': '1912-06-23',
    }
    formset = MinArticleFormSet(data)
    print formset.is_valid()
    print formset.errors
    print formset.non_form_errors()
    return render(request, 'form/articleformset.html', {'formset': formset})
#
# 表单的排序和删除行为¶
#
# formset_factory()提供两个可选参数can_order 和can_delete 来实现表单集中表单的排序和删除。
def formset_can_order(request):
    data= {
        'form-TOTAL_FORMS': '3',
        'form-INITIAL_FORMS': '2',
        'form-MAX_NUM_FORMS': '',
        'form-0-title': 'Article #1',
        'form-0-pub_date': '2008-05-10',
        'form-0-ORDER': '2',
        'form-1-title': 'Article #2',
        'form-1-pub_date': '2008-05-11',
        'form-1-ORDER': '1',
        'form-2-title': 'Article #3',
        'form-2-pub_date': '2008-05-01',
        'form-2-ORDER': '0',
    }
    ArticleFormSetOrder = formset_factory(ArticleForm,can_order=True)
    formset = ArticleFormSetOrder(data,initial=[
        {'title':'Article #1','pub_date':datetime.date(2008,5,10)},
        {'title':'Article #2','pub_date':datetime.date(2008,5,11)},
    ])
    if formset.is_valid():
        for form in formset.ordered_forms:
            print(form.cleaned_data)
    return render(request, 'form/articleformset.html', {'formset': formset})

def formset_can_delete(request):
    data= {
        'form-TOTAL_FORMS': '3',
        'form-INITIAL_FORMS': '2',
        'form-MAX_NUM_FORMS': '',
        'form-0-title': 'Article #1',
        'form-0-pub_date': '2008-05-10',
        'form-0-DELETE': 'on',
        'form-1-title': 'Article #2',
        'form-1-pub_date': '2008-05-11',
        'form-1-DELETE': '',
        'form-2-title': 'Article #3',
        'form-2-pub_date': '2008-05-01',
        'form-2-DELETE': '',
    }
    ArticleFormSetDelete = formset_factory(ArticleForm,can_delete=True)
    formset = ArticleFormSetDelete(data,initial=[
        {'title': 'Article #1', 'pub_date': datetime.date(2008, 5, 10)},
        {'title': 'Article #2', 'pub_date': datetime.date(2008, 5, 11)},
    ])
    for form in formset.deleted_forms:
        print form.cleaned_data
    instances = formset.save(commit = False)
    for obj in formset.deleted_objects:
         obj.delete()

    return render(request, 'form/articleformset.html', {'formset': formset})

def formset_add_fields(request):
    AddFormSet = formset_factory(ArticleForm,formset=AddArticleFormSet)
    formset = AddFormSet()
    return render(request, 'form/articleformset.html', {'formset': formset})

def formset_myarticleform(request):
    class MyArticleForm(ArticleForm):
        def __init__(self,*args,**kwargs):
            self.user = kwargs.pop('user')
            super(MyArticleForm,self).__init__(*args,**kwargs)
    ArticleFormSet = formset_factory(MyArticleForm)
    formset = ArticleFormSet(form_kwargs={'user':request.user})
    from django.forms import BaseFormSet
    class BaseArticleFormSet(BaseFormSet):
        def get_form_kwargs(self,index):
            kwargs = super(BaseArticleFormSet, self).get_form_kwargs(index)
            kwargs['custom_kwarg'] = index
            return kwargs
    return render(request, 'form/articleformset.html', {'formset': formset})
def manage_articles(request):
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST,request.FILES)
        if formset.is_valid():
            pass
        else:
            formset = ArticleFormSet()
    return render(request, 'form/manage_articles.html', {'formset': formset})
#视图中使用多个表单集

# 可以在视图中使用多个表单集，表单集从表单中借鉴了很多方法你可以使用
# prefix 给每个表单字段添加前缀，以允许多个字段传递给视图，而不发生命名冲突 让我们看看可以怎么做

#以以正常的方式渲染模板。记住 prefix 在POST请求和非POST 请求中均需设置，以便他能渲染和执行正确
def manage_articles(request):
    ArticleFormSet = formset_factory(ArticleForm)
    BookFormSet = formset_factory(BookForm)
    if request.method == 'POST':
        article_formset = ArticleFormSet(request.POST, request.FILES, prefix='articles')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if article_formset.is_valid() and book_formset.is_valid():
            # do something with the cleaned_data on the formsets.
            pass
    else:
        article_formset = ArticleFormSet(prefix='articles')
        book_formset = BookFormSet(prefix='books')
    return render(request, 'manage_articles.html', {
        'article_formset': article_formset,
        'book_formset': book_formset,
    })
