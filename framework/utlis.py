# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os,errno


class Uploader(object):
    def __init__(self,request,fileField,config,type="upload"):
        self.__request=request
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
        self.__stateMap=["SUCCESS",
                         "文件大小超出 upload_max_filesize 限制",
                         "文件大小超出 MAX_FILE_SIZE 限制",
                         "文件未被完整上传",
                         "没有文件被上传",
                         "上传文件为空",
                         {"ERROR_TMP_FILE":"临时文件错误"},
                         {"ERROR_TMP_FILE_NOT_FOUND":"找不到临时文件"},
                         {"ERROR_SIZE_EXCEED":"文件大小超出网站限制"},
                         {"ERROR_TYPE_NOT_ALLOWED": "文件类型不允许"},
                         {"ERROR_CREATE_DIR":"目录创建失败"},
                         {"ERROR_DIR_NOT_WRITEABLE":"目录没有写权限"},
                         {"ERROR_FILE_MOVE":"文件保存时出错"},
                         {"ERROR_FILE_NOT_FOUND":"找不到上传文件"},
                         {"ERROR_WRITE_CONTENT":"写入文件内容错误"},
                         {"ERROR_UNKNOWN":"未知错误"},
                         {"ERROR_DEAD_LINK":"链接不可用"},
                         {"ERROR_HTTP_LINK":"链接不是http链接"},
                         {"ERROR_HTTP_CONTENTTYPE":"链接contentType不正确"},
                         {"INVALID_URL":"非法 URL"},
                         {"INVALID_IP":"非法 IP"}]
        self.__type = type
        if self.__type == 'remote':
            self.__saveRemote()
        elif type == 'base64':
            self.__upBase64()
        else:
            self.__upFile()
    def __saveRemote(self):
        pass
    def __upBase64(self):
        pass
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
        if not os.path.exists(_dirname):
            try:
                os.makedirs(_dirname)
            except OSError as exc:
                self.__stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
                return




    def __getStateInfo(self,error_info):
        pass
    def __getFileExt(self):
        pass
    def __getFullName(self):
        pass
    def __getFilePath(self):
        pass
    def __getFileName(self):
        pass
    def __checkSize(self):
        pass
