# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView
from django.views.generic.detail import DetailView,SingleObjectMixin,BaseDetailView,SingleObjectTemplateResponseMixin
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView,UpdateView,DeleteView,FormMixin
from django.views.generic.dates import YearArchiveView,MonthArchiveView,WeekArchiveView,\
    DayArchiveView,TodayArchiveView,DateDetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from base_view.models import *
from base_view.forms import *
import csv
def thanks(request):
    return HttpResponse('success')

#Python自带了CSV库，csv。在Django中使用它的关键是，csv模块的CSV创建功能作用于类似于文件
# 的对象，并且Django的HttpResponse对象就是类似于文件的对象
def some_view(request):
    response=HttpResponse(content_type='test/csv')
    response['Content-Disposition']='attachment;filename="somefilename.csv"'
    writer=csv.writer(response)
    writer.writerow(['First row','Foo','Bar','Baz'])
    writer.writerow(['Second row','A','B','C','"Testing"',"Here's a quote"])
    return response
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
#流式传输大尺寸CSV文件
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

#SingleObjectMixin 与ListView 一起使用

# ListView提供内建的分页，但是可能你分页的列表中每个对象都与另外一个对象（通过一个外键）关联。在我们的Publishing
# 例子中，你可能想通过一个特定的Publisher
# 分页所有的Book。
#
# 一种方法是组合ListView
# 和SingleObjectMixin，这样分页的Book
# 列表的查询集能够与找到的单个Publisher
# 对象关联。为了实现这点，我们需要两个不同的查询集：get_queryset() get_object()

# 我们必须仔细考虑get_context_data()。因为SingleObjectMixin和ListView都会将Context数据
# 的context_object_name下，我们必须显式确保Publisher位于Context数据中。ListView将为我们
# 添加合适的page_obj和paginator ，只要我们记住调用super()。
class PublisherDetail(SingleObjectMixin,ListView):
    paginate_by = 2
    template_name = 'books/publisher_list.html'
    #注意我们 在 get()方法里设置了self.object ，这样我们就可以在后面的 get_context_data()
    #和get_queryset()方法里再次用到它. 如果不设置 template_name, 那模板会指向默认的
    #ListView 所选择的模板, 也就是 "books/book_list.html"，因为这个模板是书目的一个列表;
    #但ListView 对于该类继承了 SingleObjectMixin这个类是一无所知的,
    #所以不会对使用Publisher来查看视图有任何反应.
    def get(self,request,*args,**kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super(PublisherDetail, self).get(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context=super(PublisherDetail,self).get_context_data(**kwargs)
        context['publisher']=self.object
        return context
    def get_queryset(self):
        return self.object.book_set.all()
##########################################################################################################
#使用 FormMixin 与 DetailView
# 想想我们之前合用 View 和SingleObjectMixin 的例子. 我们想要记录用户对哪些作者感兴趣; 也就是说我们想让用户发表说为什么喜欢这些作者的信息。同样的，我们假设这些数据并没有存放在关系数据库里，而是存在另外一个奥妙之地（其实这里不用关心具体存放到了哪里）。
#
# 要实现这一点，自然而然就要设计一个 Form，让用户把相关信息通过浏览器发送到Django后台。 另外，我们要巧用REST方法,这样我们就可以用相同的URL来显示作者和捕捉来自用户的消息了。 让我们重写 AuthorDetailView 来实现它。
#
# 我们将保持DetailView的GET处理，虽然我们必须在上下文数据中添加一个Form，以便我们可以渲染它模板。我们还想从FormMixin中提取表单处理，并写一些代码，以便在POST上适当地调用表单。
#
# 注意
#
# 我们使用FormMixin并实现post()，而不是尝试将DetailView与FormView 结合(FormView已经提供了post()），因为这两个视图都实现了get()，事情会变得更加混乱。
#
# 我们的新AuthorDetail看起来像这样：
class AuthorDetail(FormMixin,DetailView):
    model = Author
    form_class = AuthorInterestForm
    # 只是提供重定向的地方，它在form_valid()的默认实现中使用。如上所述，我们必须提供我们自己的post()，
    # 并覆盖get_context_data()，以使表单在上下文数据中可用。
    def get_success_url(self):
        return reverse('author-detail',kwargs={'pk':self.object.pk})
    def get_context_data(self, **kwargs):
        context=super(AuthorDetail,self).get_context_data(**kwargs)
        context['form']=self.get_form()
        return context
    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(AuthorDetail,self).form_valid(form)

class AuthorDisplay(DetailView):
    model = Author
    def get_context_data(self, **kwargs):
        context = super(AuthorDisplay,self).get_context_data(**kwargs)
        context['form']=AuthorInterestForm()
        return context

class AuthorInterest(SingleObjectMixin,FormView):
    template_name = 'books/author_detail.html'
    form_class = AuthorInterestForm
    model = Author
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object=self.get_object()
        return super(AuthorInterest,self).post(request,*args,**kwargs)
    def get_success_url(self):
        return reverse('author-detail',kwargs={'pk':self.object.pk})
#最后，我们将这个在一个新的AuthorDetail视图中。我们已经知道，在基于类的视图上调用as_view()会让我们看起来像一个基于函数的视图，所以我们可以在两个子视图之间选择。
#您当然可以以与在URLconf中相同的方式将关键字参数传递给as_view()，例如，如果您希望AuthorInterest行为也出现在另一个网址但使用不同的模板：
class AuthorDetailView(View):
    def get(self,request,*args,**kwargs):
        view=AuthorDisplay.as_view()
        return view(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        view = AuthorInterest.as_view()
        return view(request,*args,**kwargs)
#################################################################################
from generic.views import JSONResponseMixin
class JSONView(JSONResponseMixin,TemplateView):
    def render_to_response(self,context,**response_kwargs):
        return self.render_to_json_response(context,**response_kwargs)

class JSONDetailView(JSONResponseMixin,BaseDetailView):
    def render_to_response(self,context,**response_kwargs):
        return self.render_to_json_response(context,**response_kwargs)
#如果你想更进一步，你可以组合DetailView 的子类，它根据HTTP 请求的某个属性既能够返回HTML 又能够返回JSON 内容，
# 例如查询参数或HTTP 头部。这只需将JSONResponseMixin 和SingleObjectTemplateResponseMixin 组合，
# 并覆盖render_to_response() 的实现以根据用户请求的响应类型进行正确的渲染：
class HybridDetailView(JSONResponseMixin,SingleObjectTemplateResponseMixin,BaseDetailView):
    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('format')=='json':
            return self.render_to_json_response(context,**response_kwargs)
        else:
            return super(HybridDetailView,self).render_to_response(context)


