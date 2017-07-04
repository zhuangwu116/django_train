# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,render_to_response
from .models import ArticleCategory
from .forms import *
from django.template.response import TemplateResponse
# Create your views here.
def addindex(request):
    objects=ArticleCategory.objects.filter(parent__isnull=True)
    return render(request,'testdemo.html',{'categoryList':objects})
def getmenu(request):
    if request.is_ajax():
        if request.method=='GET':
            if 'id' in request.GET:
                id=request.GET['id']
                select_count=request.GET['select_count']
                if id=='null':
                    objects=ArticleCategory.objects.filter(parent__isnull=True)
                    return render_to_response('select_ajax.html',{'count':select_count,'categoryList':objects})
                if id:
                    objects=ArticleCategory.objects.filter(parent=id)
                    if len(objects)>0:
                        return render_to_response('select_ajax.html',{'count':select_count,'categoryList':objects})

    return HttpResponse('')
def addmenu(request):
    if request.method=='POST':
        name=request.POST['name']
        id=request.POST['id']
        if id=='null':
            objects=ArticleCategory(name=name)
        else:
            parent=ArticleCategory.objects.filter(id=id).first()
            objects=ArticleCategory(name=name,parent=parent)
        objects.save()
        return HttpResponse('测试成功')
def menuindex(request):
    objects=ArticleCategory.menuobjects.premenu('a')
    return render(request,'menuindex.html',locals())
def getpostlist(request):
    if request.method=="POST":
        idlists=request.POST.getlist('_selected_action')
        for id in idlists:
            menu=ArticleCategory.objects.filter(id=id).first()
            if menu:
                menu.delete()
    else:
        id=request.GET.get('id')
        if id:
            menu = ArticleCategory.objects.filter(id=id).first()
            if menu:
                menu.delete()
    menulist = ArticleCategory.menuobjects.menu()
    return render(request,'postlist.html',locals())
def test_form(request):
    return render(request,'test_form.html',{'form':TestForm()})

def index(request,template='index.html',extra_context=None):
    context={"username":'zhuangwu'}
    context.update(extra_context or {})
    return TemplateResponse(request,template,context)
def post_list(request,template='postlist.html',extra_context=None):
    if request.method == "POST":
        idlists = request.POST.getlist('_selected_action')
        for id in idlists:
            menu = ArticleCategory.objects.filter(id=id).first()
            if menu:
                menu.delete()
    else:
        id = request.GET.get('id')
        if id:
            menu = ArticleCategory.objects.filter(id=id).first()
            if menu:
                menu.delete()
    menulist = ArticleCategory.menuobjects.menu()
    context={"menulist":menulist}
    context.update(extra_context or {})
    return TemplateResponse(request,template,context)


from djangtestdemo import models
# Create your views here.
def video(request,*args,**kwargs):
    condition={}
    for k,v in kwargs.items():
        condition[k]=int(v)
        kwargs[k]=int(v)#重新以字典的方式赋值
        print k,v
    print kwargs,args,"zhuangwu"
    class_list=models.Classification.objects.all()
    level_list=models.Level.objects.all()
    video_list=models.Video.objects.filter(**condition)#筛选的地方
    return render(request,"video.html",{"class_list":class_list,
                                        "level_list":level_list,
                                        "kwargs":kwargs,
                                        "video_list":video_list})

def page(request,page_number,page=None):
    return HttpResponse(page_number)

