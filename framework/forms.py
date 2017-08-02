from __future__ import unicode_literals

from django.forms import Widget
from .static import static_lazy as static
from django import forms
from uuid import uuid4


class UeditorWidget(Widget):
    template_name = 'framework/ueditor/ueditor.html'


class UeditorInput(UeditorWidget):
    class Media:
        js = [static("ueditor/ueditor.config.js"),
              static("ueditor/ueditor.all.js"),
              static("ueditor/lang/zh-cn/zh-cn.js"),
              static("ueditor/ueditor.parse.js")]
        css ={'all':[static("ueditor/themes/default/css/ueditor.css")]}
class UeditorForm(forms.Form):
    title = forms.CharField(max_length=50,widget=forms.TextInput(attrs={"id":"title",}))
    content = forms.CharField(max_length=5000,widget=UeditorInput(attrs={"id":"container",}))



def get_edit_form(obj, field_names, data=None, files=None):
    widget_overrides = {
        forms.Textarea:UeditorInput
    }
    class EditForm(forms.ModelForm):

        app = forms.CharField(widget=forms.HiddenInput)
        model = forms.CharField(widget=forms.HiddenInput)
        id = forms.CharField(widget=forms.HiddenInput)
        fields = forms.CharField(widget=forms.HiddenInput)

        class Meta:
            model = obj.__class__
            fields = field_names.split(",")

        def __init__(self, *args, **kwargs):
            super(EditForm,self).__init__(*args, **kwargs)
            self.uuid = str(uuid4())
            for f in self.fields.keys():
                field_class = self.fields[f].widget.__class__
                print field_class
                try:
                    widget = widget_overrides[field_class]
                except KeyError:
                    pass
                else:
                    self.fields[f].widget = widget()
                css_class = self.fields[f].widget.attrs.get("class","")
                css_class += " " + field_class.__name__.lower()
                self.fields[f].widget.attrs["class"] = css_class
                self.fields[f].widget.attrs["id"] = "%s-%s" % (f,self.uuid)
                if self.fields[f].required:
                    self.fields[f].widget.attrs["required"] = ""
    initial = {
        "app":obj._meta.app_label,"id":obj.id,
        "fields":field_names,"model":obj._meta.object_name.lower()
    }
    return EditForm(instance=obj,initial=initial,data=data,files=files)