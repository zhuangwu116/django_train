from __future__ import unicode_literals

from django.forms import Widget
from django.utils.html import format_html
from django.forms.utils import flatatt,force_text
from .static import static_lazy as static
from django import forms
class UeditorWidget(Widget):
    template_name = 'framework/ueditor/ueditor.html'


class UeditorInput(UeditorWidget):
    class Media:
        js = [static("ueditor/ueditor.config.js"),
              static("ueditor/ueditor.all.js"),
              static("ueditor/lang/zh-cn/zh-cn.js")]
        css ={'all':[static("ueditor/themes/default/css/ueditor.css")]}
class UeditorForm(forms.Form):
    title = forms.CharField(max_length=50,widget=forms.TextInput(attrs={"id":"title",}))
    content = forms.CharField(max_length=5000,widget=UeditorInput(attrs={"id":"container",}))