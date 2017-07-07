from django.conf.urls import url
from base_view import views
from django.views.generic import TemplateView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import DateDetailView
from base_view.models import *
urlpatterns=[
    url(r'^index$',TemplateView.as_view(template_name='base_view/index.html'),name='index'),
    url(r'^myview/(?P<pk>\d+)$',views.MyView.as_view(),name='myview'),
    url(r'^homepageview/(?P<id>\d+)$',views.HomePageView.as_view(),name='homepageview'),
    url(r'^counter/(?P<pk>[0-9]+)/$', views.ArticleCounterRedirectView.as_view(), name='article-counter'),
    url(r'^(?P<pk>[0-9]+)/$',views.ArticleDetailView.as_view(),name='article-detail'),
    url(r'^article_list$',views.ArticleListView.as_view(),name='article-list'),

    url(r'^article_list_filter/([\w-]+)/$',views.ArticleListfilter.as_view(),name='article_list_filter'),

    url(r'^thanks/$', views.thanks, name='thanks'),

    url(r'^formview/$', views.ArticleFormView.as_view(), name='formview'),
    url(r'^createview/$', views.ArticleCreateView.as_view(), name='createview'),
    url(r'^updateview/(?P<pk>[0-9]+)/$', views.ArticleUpdateView.as_view(), name='updateview'),
    url(r'^deleteview/(?P<pk>[0-9]+)/$',views.ArticleDeleteView.as_view(),name='deleteview'),
    url(r'^archive_index/$', ArchiveIndexView.as_view(model=Article,date_field="create_at",template_name='base_view/article_archive.html'),
        name='archive_index'),

    url(r'^archive_year/(?P<year>[0-9]{4})/$',views.ArticleYearArchiveView.as_view(),name='archive_year'),

    url(r'^archive_month/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',views.ArticleMonthArchiveView.as_view(month_format='%m'),name='archive_month'),
    url(r'^archive_week/(?P<year>[0-9]{4})/(?P<week>[0-9]+)/$',
        views.ArticleWeekArchiveView.as_view(), name='archive_week'),
    url(r'^archive_day/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$',
        views.ArticleDayArchiveView.as_view(), name='archive_day'),

    url(r'^archive_date_detail/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/$',
        DateDetailView.as_view(template_name='base_view/article_detail.html',model=Article, date_field="pub_date"),
        name="archive_date_detail"),

url(r'^index_login$',views.ProtectedView.as_view(),name='index_login'),
]