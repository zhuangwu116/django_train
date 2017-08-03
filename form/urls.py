# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from form import views
urlpatterns=[
    url(r'^$',views.send_mail,name="index"),
    url(r'^articleformset$',views.articleformset,name="articleformset"),
    url(r'^formset_validation$',views.formset_validation,name="formset_validation"),
    url(r'^customformset_valid$',views.customformset_valid,name="customformset_valid"),
    url(r'^formset_validate_max$',views.formset_validate_max,name="formset_validate_max"),
    url(r'^formset_validate_min$',views.formset_validate_min,name="formset_validate_min"),
    url(r'^formset_can_order$',views.formset_can_order,name="formset_can_order"),
    url(r'^formset_can_delete$',views.formset_can_delete,name="formset_can_delete"),
    url(r'^formset_add_fields$', views.formset_add_fields, name="formset_add_fields"),
]