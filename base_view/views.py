# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView,UpdateView,DeleteView
from django.views.generic.dates import YearArchiveView,MonthArchiveView,WeekArchiveView,\
    DayArchiveView,TodayArchiveView,DateDetailView


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

#http://127.0.0.1:8000/base_view/article_list?page=2
class ArticleListView(ListView):
    #指定model = Article等价于快速声明的queryset = Article.objects.all()。
    model = Article
    paginate_by = 3
    allow_empty = True
    context_object_name = 'article_objs'
    template_name = 'base_view/article_list.html'
    def get_context_data(self, **kwargs):
        context=super(ArticleListView,self).get_context_data(**kwargs)
        return context
#显示表单的视图。发送错误时，重新显示表单和验证的错误；成功时，重定向到一个新的URL。
class ArticleFormView(FormView):

    template_name = 'base_view/article_form.html'
    form_class = ArticleForm
    initial = {"title":"title","context":"context","create_at":timezone.now(),}
    success_url = '/base_view/thanks/'

    def form_valid(self, form):
        print 'articleformview'
        print form.cleaned_data['title']
        print form.cleaned_data['context']
        print form.cleaned_data['create_at']
        return super(ArticleFormView,self).form_valid(form)

class ArticleCreateView(CreateView):
    model = Article
    #fields这是一个必需的属性，如果你是自动生成表单类（例如。使用model）。省略此属性将导致ImproperlyConfigured异常。
    fields = ['title','context','create_at']
    success_url = '/base_view/thanks/'
    template_name = 'base_view/article_form.html'

    def form_valid(self, form):
        print "ArticleCreateView"
        return super(ArticleCreateView,self).form_valid(form)

    def form_invalid(self, form):

        return super(ArticleCreateView,self).form_invalid(form)

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'context', 'create_at']
    template_name = 'base_view/article_form.html'


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('base_view:article-list')
    template_name = 'base_view/article_delete.html'


#一个年度归档页面，显示给定年份中的所有可用月份。除非您将allow_future设置为True，否则不会显示未来中日期的对象。

# make_object_list
# 一个布尔值，指定是否检索今年的完整对象列表，并将其传递给模板。如果True，对象列表将可用于上下文。如果False，则None查询集将用作对象列表。默认情况下，这是False。
#
# get_make_object_list()
# 确定对象列表是否将作为上下文的一部分返回。默认返回make_object_list。
#
# 上下文
#
# 除了django.views.generic.list.MultipleObjectMixin（通过django.views.generic.dates.BaseDateListView）提供的上下文，模板的上下文将是：
#
# date_list: A DateQuerySet object containing all months that have objects available according to queryset, represented as datetime.datetime objects, in ascending order.
# year：代表给定年份的date对象。
# next_year：根据allow_empty和allow_future，表示下一年第一天的date对象。
# previous_year：根据allow_empty和allow_future，表示上一年第一天的date对象。
# 备注
#
# 使用_archive_year的默认template_name_suffix。
class ArticleYearArchiveView(YearArchiveView):
    queryset = Article.objects.all()
    date_field = 'create_at'
    make_object_list = True
    allow_future = True
    template_name = 'base_view/article_archive_year.html'
#显示给定月份中所有对象的月度归档页面。除非您将allow_future设置为True，否则不会显示未来中日期的对象。

# 上下文
#
# 除了MultipleObjectMixin（通过BaseDateListView）提供的上下文，模板的上下文将是：
#
# date_list: A DateQuerySet object containing all days that have objects available in the given month, according to queryset, represented as datetime.datetime objects, in ascending order.
# month：表示给定月份的date对象。
# next_month：根据allow_empty和allow_future，表示下个月第一天的date对象。
# previous_month：根据allow_empty和allow_future，表示上个月第一天的date对象。
# 备注
#
# 使用_archive_month的默认template_name_suffix。
class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Article.objects.all()
    date_field = 'create_at'
    allow_future = True
    template_name = 'base_view/article_archive_month.html'


#显示给定周内所有对象的每周归档页面。除非您将allow_future设置为True，否则不会显示未来中日期的对象。
# 上下文
#
# 除了MultipleObjectMixin（通过BaseDateListView）提供的上下文，模板的上下文将是：
#
# week：表示给定周的第一天的date对象。
# next_week：根据allow_empty和allow_future表示下周第一天的date对象。
# previous_week：根据allow_empty和allow_future，表示前一周第一天的date对象。
# 备注
#
# 使用_archive_week的默认template_name_suffix。
class ArticleWeekArchiveView(WeekArchiveView):
    queryset = Article.objects.all()
    date_field = 'create_at'
    allow_future = True
    week_format = '%W'
    template_name = 'base_view/article_archive_week.html'

#显示指定日期内所有对象的日期归档页面。除非您将allow_future设置为True，否则以后的日期都会抛出404错误，而不管以后是否存在任何对象。
#
#
# 上下文
#
# 除了MultipleObjectMixin（通过BaseDateListView）提供的上下文，模板的上下文将是：
#
# day：代表给定日期的date对象。
# next_day：根据allow_empty和allow_future，表示第二天的date对象。
# previous_day：表示前一天的date对象，根据allow_empty和allow_future。
# next_month：根据allow_empty和allow_future，表示下个月第一天的date对象。
# previous_month：根据allow_empty和allow_future，表示上个月第一天的date对象。
# 备注
#
# 使用_archive_day的默认template_name_suffix。

#http://127.0.0.1:8000/base_view/archive_day/2017/jul/04/
class ArticleDayArchiveView(DayArchiveView):
    queryset = Article.objects.all()
    date_field = 'create_at'
    allow_future = True
    template_name = 'base_view/article_archive_day.html'
