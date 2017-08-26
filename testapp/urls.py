# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from testapp import views
urlpatterns=[
    url(r'^test_checkbox$', views.test_checkbox, name="test_checkbox"),
]