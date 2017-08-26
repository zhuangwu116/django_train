# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def test_checkbox(request):
    if request.method == "POST":
        if request.POST.get("test"):
            print "true"
        else:
            print "flase"
    return render(request,"testapp/checkbox.html",{})