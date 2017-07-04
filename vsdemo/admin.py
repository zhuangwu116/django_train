# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from vsdemo.models import Choice,Poll
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields':['text']}),
        ('Date information',{'fields':['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('text','pub_date')
    list_filter = ['pub_date']
    search_fields = ['text']
    date_hierarchy = 'pub_date'


admin.site.register(Poll,PollAdmin)