# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView
from django.views.generic.detail import DetailView,SingleObjectMixin
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView,UpdateView,DeleteView
from django.views.generic.dates import YearArchiveView,MonthArchiveView,WeekArchiveView,\
    DayArchiveView,TodayArchiveView,DateDetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
    # 指定model = Article等价于快速声明的queryset = Article.objects.all()。
    model = Article
    template_name = 'base_view/article_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        context['now']=timezone.now()
        return context
#以上面等价
class ArticleDetail(DetailView):
    # 指定model = Article等价于快速声明的queryset = Article.objects.all()。
    queryset = Article.objects.all()
    template_name = 'base_view/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ArticleDetail_get_obj(DetailView):
    # 指定model = Article等价于快速声明的queryset = Article.objects.all()。
    queryset = Article.objects.all()
    template_name = 'base_view/article_detail.html'
    def get_object(self):
        object=super(ArticleDetail_get_obj,self).get_object()
        object.create_at=timezone.now()
        object.save()
        return object

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

# http://127.0.0.1:8000/base_view/article_list?page=2
class ArticleList(ListView):
    # 指定model = Article等价于快速声明的queryset = Article.objects.all()。
    queryset = Article.objects.order_by('-id')
    paginate_by = 3
    allow_empty = True
    context_object_name = 'article_objs'
    template_name = 'base_view/article_list.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        return context
#动态过滤
class ArticleListfilter(ListView):
    template_name = 'base_view/article_list.html'
    def get_queryset(self):
        self.title=get_object_or_404(Article,self.args[0])
        return Article.objects.filter(title__contains=self.title)
    def get_context_data(self, **kwargs):
        context=super(ArticleListfilter,self).get_context_data(**kwargs)
        context['title']=self.title
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
    #这里我们必须使用reverse_lazy() 而不是reverse，因为在该文件导入时URL 还没有加载。
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


# @method_decorator(never_cache, name='dispatch')
# @method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'base_view/index.html'
    @method_decorator(login_required(login_url='/admin/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProtectedView,self).dispatch(request,*args,**kwargs)

#在这个视图中，请确保你没有将created_by 包含进要编辑的字段列表，并覆盖form_valid() 来添加这个用户：
class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(AuthorCreate, self).form_valid(form)




from generic.views import AjaxableResponseMixin

class AJAXAuthorCreate(AjaxableResponseMixin,CreateView):
    model = Article
    fields = ['title', 'context', 'create_at']
    template_name = 'base_view/ajaxableresponsemixin.html'

#SingleObjectMixin 与View 一起使用

#如果你想编写一个简单的基于类的视图，它只响应POST，我们将子类化View 并在子类中只编写一个post()
# 方法。但是，如果我们想处理一个由URL 标识的特定对象，我们将需要SingleObjectMixin 提供的功能。
class RecordInterest(SingleObjectMixin,View):
    model = Article
    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object=self.get_object()
        return HttpResponseRedirect(reverse('base_view:article-detail',kwargs={'pk':self.object.pk}))