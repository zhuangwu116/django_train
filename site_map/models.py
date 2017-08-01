# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.sitemaps import Sitemap
from base_view.models import Article
# Create your models here.
# 注意：
#
# changefreq和priority分别是对应于<changefreq>和<priority>它们可以作为函数调用，例如这个例子中的lastmod。
# items()只是一个返回对象列表的方法。返回的对象将传递给与网站地图属性（location，lastmod，changefreq和priority
# lastmod 应返回 Python datetime 对象。
# 在此示例中没有 location 方法，但你可以提供此方法来指定对象的 URL。默认情况下，location()在每个对象上调用
# get_absolute_url()并返回结果。
class BlogSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self,obj):
        return obj.create_at