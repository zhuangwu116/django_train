from django.conf.urls import url
from djangtestdemo import views
urlpatterns=[
    url(r'^addindex$', views.addindex, name='addindex'),
    url(r'^getmenu$', views.getmenu, name='getmenu'),
    url(r'^addmenu$', views.addmenu, name='addmenu'),
    url(r'^menuindex$', views.menuindex, name='menuindex'),
    url(r'^postlist$', views.getpostlist, name='postlist'),
    url(r'^testform$', views.test_form, name='test_form'),
    url(r'^index$', views.index, name='indext'),
    url(r'^post_list$', views.post_list, name='post_list'),
    url(r'^video-(?P<classification_id>(\d+))-(?P<level_id>(\d+)).html$', views.video, name='video'),
    url(r'^comments/(?:page-(?P<page_number>\d+)/)?$', views.page, name='page'),

]