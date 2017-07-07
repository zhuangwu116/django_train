# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
class LoginRequireMixin(object):
    @classmethod
    def as_view(cls,**initkwargs):
        view=super(LoginRequireMixin,cls).as_view(**initkwargs)
        return login_required(view)
class MyView(LoginRequireMixin):
    pass