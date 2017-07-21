# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import UeditorForm
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
config_json={
    "imageActionName": "uploadimage",
    "imageFieldName": "upfile",
    "imageMaxSize": 2048000,
    "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "imageCompressEnable": "true",
    "imageCompressBorder": 1600,
    "imageInsertAlign": "none",
    "imageUrlPrefix": "",
    "imagePathFormat": "/ueditor/php/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
    "scrawlActionName": "uploadscrawl",
    "scrawlFieldName": "upfile",
    "scrawlPathFormat": "/ueditor/php/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
    "scrawlMaxSize": 2048000,
    "scrawlUrlPrefix": "",
    "scrawlInsertAlign": "none",
    "snapscreenActionName": "uploadimage",
    "snapscreenPathFormat": "/ueditor/php/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
    "snapscreenUrlPrefix": "",
    "snapscreenInsertAlign": "none",

    "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"],
    "catcherActionName": "catchimage",
    "catcherFieldName": "source",
    "catcherPathFormat": "/ueditor/php/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
    "catcherUrlPrefix": "",
    "catcherMaxSize": 2048000,
    "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],

    "videoActionName": "uploadvideo",
    "videoFieldName": "upfile",
    "videoPathFormat": "/ueditor/php/upload/video/{yyyy}{mm}{dd}/{time}{rand:6}",
    "videoUrlPrefix": "",
    "videoMaxSize": 102400000,
    "videoAllowFiles": [
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"],

    "fileActionName": "uploadfile",
    "fileFieldName": "upfile",
    "filePathFormat": "/ueditor/php/upload/file/{yyyy}{mm}{dd}/{time}{rand:6}",
    "fileUrlPrefix": "",
    "fileMaxSize": 51200000,
    "fileAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ],

    "imageManagerActionName": "listimage",
    "imageManagerListPath": "/ueditor/php/upload/image/",
    "imageManagerListSize": 20,
    "imageManagerUrlPrefix": "",
    "imageManagerInsertAlign": "none",
    "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "fileManagerActionName": "listfile",
    "fileManagerListPath": "/ueditor/php/upload/file/",
    "fileManagerUrlPrefix": "",
    "fileManagerListSize": 20,
    "fileManagerAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ]
}
def index(request):
    if request.method == "POST":
        form = UeditorForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["content"])
    else:
        form = UeditorForm(initial={"content": "<p>aaaaaaaaaaaaaaaaaaaaa</p>"})
    return render(request,'framework/index.html',{"form":form})
@csrf_exempt
def controller(request):
    action = request.GET.get("action")
    if action == 'config':
        return JsonResponse(config_json)
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
    return HttpResponse(status=200)