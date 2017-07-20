# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import UeditorForm
from django.http import HttpResponse
import json
import os
from django11_test.settings import BASE_DIR

# Create your views here.
def index(request):
    form=UeditorForm(initial={"content":"<p>aaaaaaaaaaaaaaaaaaaaa</p>"})
    if request.method == "POST":
        form = UeditorForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["content"])
        else:
            print("aaaaa")
    return render(request,'framework/index.html',{"form":form})

def controller(request):
    if request.method == "GET":
        action = request.GET.get("action")
        if action == 'config':
            JSON_FILE = os.path.join(os.path.dirname(__file__),'config.json')
            with open(JSON_FILE,'r') as json_file:
                data = json.load(json_file)
            return HttpResponse(data,content_type='application/json')
        elif action == 'uploadimage':
            pass
        elif action == 'uploadscrawl':
            pass
        elif action == 'uploadvideo':
            pass
        elif action == 'uploadfile':
            pass
        elif action == 'listimage':
            pass
        elif action == 'listfile':
            pass
        elif action == 'catchimage':
            pass
        else:
            pass
    return HttpResponse(status=500)