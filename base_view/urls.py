from django.conf.urls import url
from base_view import views
from django.views.generic import TemplateView
urlpatterns=[
    url(r'^index$',TemplateView.as_view(template_name='base_view/index.html'),name='index'),
    url(r'^myview/(?P<pk>\d+)$',views.MyView.as_view(),name='myview'),
    url(r'^homepageview/(?P<id>\d+)$',views.HomePageView.as_view(),name='homepageview'),
    url(r'^counter/(?P<pk>[0-9]+)/$', views.ArticleCounterRedirectView.as_view(), name='article-counter'),
    url(r'^(?P<pk>[0-9]+)/$',views.ArticleDetailView.as_view(),name='article-detail'),
    url(r'^article_list$',views.ArticleListView.as_view(),name='article-list'),

    url(r'^thanks/$', views.thanks, name='thanks'),

    url(r'^formview/$', views.ArticleFormView.as_view(), name='thanks'),

]