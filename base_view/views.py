# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import View,TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from base_view.models import *
from base_view.forms import *

def thanks(request):
    return HttpResponse('success')


class MyView(View):
    http_method_names = ['post','get']
    def dispatch(self, request, *args, **kwargs):
      return super(MyView,self).dispatch(request,*args,**kwargs)
    def get(self,request,*args,**kwargs):
        pk=kwargs.pop('pk')
        print 'myview',pk
        return render(request,'base_view/index.html',{})


class HomePageView(TemplateView):
    template_name = 'base_view/home.html'

    def get_context_data(self, **kwargs):
        id=kwargs.pop('id')
        print 'homepageview',id
        context=super(HomePageView,self).get_context_data(**kwargs)
        context['title']='HomePageView'
        return context

class ArticleCounterRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'base_view:myview'
    def get_redirect_url(self, *args, **kwargs):
        article=get_object_or_404(Article,pk=kwargs['pk'])
        return super(ArticleCounterRedirectView, self).get_redirect_url(*args, **kwargs)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'base_view/article_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        context['now']=timezone.now()
        return context


class ArticleListView(ListView):
    model = Article
    paginate_by = 3
    allow_empty = True
    template_name = 'base_view/article_list.html'
    def get_context_data(self, **kwargs):
        context=super(ArticleListView,self).get_context_data(**kwargs)
        return context
#显示表单的视图。发送错误时，重新显示表单和验证的错误；成功时，重定向到一个新的URL。
class ArticleFormView(FormView):
    template_name = 'base_view/article_form.html'
    form_class = ArticleForm
    success_url = '/base_view/thanks/'

    def form_valid(self, form):
        print 'articleformview'
        print form.cleaned_data['title']
        print form.cleaned_data['context']
        print form.cleaned_data['create_at']
        return super(ArticleFormView,self).form_valid(form)

