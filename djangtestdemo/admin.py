# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from djangtestdemo.models import *
# Register your models here.
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['treenode', 'patha', 'id', 'serialnumber']
    ordering = ['path']
    def patha(self, obj):
        if obj.parent:
            return u'%s > %s' % (obj.parent, obj.name)
        return obj.name
    patha.short_description = 'path'
    patha.allow_tags = True

    def treenode(self, obj):
        indent_num = len(obj.path.split(':')) - 1
        p = '<div style="text-indent:%spx;">%s</div>' % (indent_num * 25, obj.name)
        return p

    treenode.short_description = 'tree path'
    treenode.allow_tags = True


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)
admin.site.register(LeiXing)


admin.site.register(Direction)
admin.site.register(Classification)
admin.site.register(Level)
admin.site.register(Video)
