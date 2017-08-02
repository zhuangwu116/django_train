# -*- coding: utf-8 -*-
from __future__ import unicode_literals



from django.conf.urls import url
from framework import views

urlpatterns=[
url(r'^$',views.index,name="index"),
    url(r'^controller$',views.controller,name='controller'),
    url(r'^edit_form$', views.get_form, name='edit_form'),
]