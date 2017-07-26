# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from form import views
urlpatterns=[
    url(r'^$',views.send_mail,name="index"),
    url(r'^articleformset$',views.articleformset,name="articleformset"),
]