# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from base_view.models import *
# Register your models here.
admin.site.register(Article)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)