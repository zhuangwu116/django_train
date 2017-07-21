from django.conf.urls import url
from framework import views

urlpatterns=[
url(r'^$',views.index,name="index"),
    url(r'^controller$',views.controller,name='controller'),
]