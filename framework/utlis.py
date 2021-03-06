# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import base64
import random
from datetime import datetime
from django.utils.safestring import mark_for_escaping
from  tasks import request_http
from celery.utils.log import get_logger
logger = get_logger(__name__)
def handle_uploaded_file(f,path):
    with open(path,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class Uploader(object):
    def __init__(self,request,fileField,config,rootPath,type="upload"):
        self.__request=request
        self.__rootPath = rootPath
        self.__fileField = fileField
        self.__file = None
        self.__base64 = None
        self.__config = config
        self.__oriName = None
        self.__fileName = None
        self.__fullName = None
        self.__filePath = None
        self.__fileSize = None
        self.__fileType = None
        self.__stateInfo = None
        self.__stateMap={"SUCCESS":"SUCCESS",
                         "UPLOAD_MAX_FILESIZE_MESSAGE":"文件大小超出 upload_max_filesize 限制",
                         "MAX_FILE_SIZE_MESSAGE":"文件大小超出 MAX_FILE_SIZE 限制",
                         "FILE_UNUPLOAD":"文件未被完整上传",
                         "UNUPLOAD_FILE":"没有文件被上传",
                         "UPLOAD_FILE_NULL":"上传文件为空",
                         "ERROR_TMP_FILE":"临时文件错误",
                         "ERROR_TMP_FILE_NOT_FOUND":"找不到临时文件",
                         "ERROR_SIZE_EXCEED":"文件大小超出网站限制",
                         "ERROR_TYPE_NOT_ALLOWED": "文件类型不允许",
                         "ERROR_CREATE_DIR":"目录创建失败",
                         "ERROR_DIR_NOT_WRITEABLE":"目录没有写权限",
                         "ERROR_FILE_MOVE":"文件保存时出错",
                         "ERROR_FILE_NOT_FOUND":"找不到上传文件",
                         "ERROR_WRITE_CONTENT":"写入文件内容错误",
                         "ERROR_UNKNOWN":"未知错误",
                         "ERROR_DEAD_LINK":"链接不可用",
                         "ERROR_HTTP_LINK":"链接不是http链接",
                         "ERROR_HTTP_CONTENTTYPE":"链接contentType不正确",
                         "INVALID_URL":"非法 URL",
                         "INVALID_IP":"非法 IP"}
        self.__type = type
        if self.__type == 'remote':
            self.__saveRemote()
        elif type == 'base64':
            self.__upBase64()
        else:
            self.__upFile()


    def __saveRemote(self):
        imgUrl = mark_for_escaping(self.__request.POST.get(self.__fileField))
        imgUrl = imgUrl.replace("&amp;","&")
        if (not imgUrl.startswith("http")) or (not imgUrl.startswith("https")) :
            self.__stateInfo = self.__getStateInfo("ERROR_HTTP_LINK")
            return
        try:
            res =  request_http.delay(imgUrl)
            http_head,http_content = res.get()
        except request_http.OperationalError as exc:
            self.__stateInfo = self.__getStateInfo("ERROR_DEAD_LINK")
            logger.exception('Sending task raised: %r',exc)
            return

        if http_head["status"] is not 200:
            self.__stateInfo = self.__getStateInfo("ERROR_DEAD_LINK")
            return
        content_type = http_head["Content-Type"]
        fileType='.'+content_type.split('/')[-1]
        if (not (fileType in self.__config['allowFiles'])) or (not (content_type.split('/')[0] == 'image')):
            self.__stateInfo = self.__getStateInfo("ERROR_HTTP_CONTENTTYPE")
            return
        self.__oriName = imgUrl.split('/')[-1]
        self.__fileSize = len(http_content)
        self.__fileType = self.__getFileExt()
        self.__fullName = self.__getFullName()
        self.__filePath = self.__getFilePath()
        self.__fileName = self.__getFileName()
        _dirname = os.path.dirname(self.__filePath)
        if not self.__checkSize():
            self.__stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
            return
        if not os.path.exists(_dirname):
            try:
                os.makedirs(_dirname, mode=0777)
            except OSError as exc:
                self.__stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
                return
        if not os.path.exists(_dirname):
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_MOVE")
            return
        try:
            with open(self.__filePath,'wb+') as f:
                f.write(http_content)
        except:
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_MOVE")
            return
        self.__stateInfo = self.__stateMap["SUCCESS"]






    def __upBase64(self):
        base64Data = self.__request.POST.get(self.__fileField)
        if not base64Data:
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_NOT_FOUND")
            return
        img = base64.b64decode(base64Data)
        self.__oriName = self.__config['oriName']
        self.__fileSize = len(img)
        self.__fileType = self.__getFileExt()
        self.__fullName = self.__getFullName()
        self.__filePath = self.__getFilePath()
        self.__fileName = self.__getFileName()
        _dirname = os.path.dirname(self.__filePath)
        if not self.__checkSize():
            self.__stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
            return
        if not os.path.exists(_dirname):
            try:
                os.makedirs(_dirname, mode=0777)
            except OSError as exc:
                self.__stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
                return
        if not os.path.exists(_dirname):
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_MOVE")
            return
        try:
            with open(self.__filePath,'wb+') as f:
                f.write(img)
        except:
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_MOVE")
            return
        self.__stateInfo = self.__stateMap["SUCCESS"]



    def __upFile(self):
        _file = self.__file = self.__request.FILES[self.__fileField]
        if not _file:
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_NOT_FOUND")
            return
        self.__oriName = _file.name
        self.__fileSize = _file.size
        self.__fileType = self.__getFileExt()
        self.__fullName = self.__getFullName()
        self.__filePath = self.__getFilePath()
        self.__fileName = self.__getFileName()
        _dirname = os.path.dirname(self.__filePath)
        if not self.__checkSize():
            self.__stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
            return
        if not self.__checkType():
            self.__stateInfo = self.__getStateInfo("ERROR_TYPE_NOT_ALLOWED")
            return
        if not os.path.exists(_dirname):
            try:
                os.makedirs(_dirname,mode=0777)
            except OSError as exc:
                self.__stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
                return
        if not os.path.exists(_dirname):
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_MOVE")
            return
        try:
            handle_uploaded_file(_file,self.__filePath)
        except:
            self.__stateInfo = self.__getStateInfo("ERROR_FILE_MOVE")
            return
        self.__stateInfo = self.__stateMap["SUCCESS"]


    def __getStateInfo(self,error_info):
        return self.__stateMap[error_info]


    def __getFileExt(self):
        return str(os.path.splitext(self.__oriName)[-1])


    def __getFullName(self):
        _t = datetime.now()
        _format = str(self.__config["pathFormat"])
        _format = _format.replace("{yyyy}",_t.strftime("%Y"))
        _format = _format.replace("{yy}", _t.strftime("%y"))
        _format = _format.replace("{mm}", _t.strftime("%m"))
        _format = _format.replace("{dd}", _t.strftime("%d"))
        _format = _format.replace("{hh}", _t.strftime("%H"))
        _format = _format.replace("{ii}", _t.strftime("%M"))
        _format = _format.replace("{ss}", _t.strftime("%S"))
        _format = _format.replace("{time}", _t.strftime("%f"))
        randNum = random.randint(1,1000000)
        _format = _format.replace("{rand:6}",str(randNum))
        ext = self.__getFileExt()
        return _format+ext
    def __getFilePath(self):
        fullname = self.__fullName
        rootPath = self.__rootPath
        if not fullname.startswith('/'):
            fullname = '/'+fullname
        return rootPath+fullname
    def __getFileName(self):
        fullname = self.__filePath
        return fullname.split("/")[-1]
    def __checkSize(self):
        return self.__fileSize <= self.__config["maxSize"]
    def __checkType(self):
        return self.__getFileExt() in self.__config["allowFiles"]

    def getFileInfo(self):
        return {
            "state":self.__stateInfo,
            "url":self.__fullName,
            "title":self.__fileName,
            "original":self.__oriName,
            "type":self.__fileType,
            "size":self.__fileSize
        }
