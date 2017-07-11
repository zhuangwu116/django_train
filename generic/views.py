# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
# Create your views here.
class LoginRequireMixin(object):
    @classmethod
    def as_view(cls,**initkwargs):
        view=super(LoginRequireMixin,cls).as_view(**initkwargs)
        return login_required(view)


from django.http import JsonResponse

class AjaxableResponseMixin(object):
    def form_invalid(self,form):
        response=super(AjaxableResponseMixin,self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors,status=400)
        else:
            return response
    def form_valid(self,form):
        self.object=form.save()
        print dir(super(AjaxableResponseMixin,self))
        response = super(AjaxableResponseMixin,self).form_invalid(form)
        if self.request.is_ajax():
            data={
                'pk':self.object.pk
            }
            return JsonResponse(data)
        else:
            return response

#基于类的视图在同一件事需要实现多次的时候非常有优势。假设你正在编写API，每个视图应该返回JSON 而不是渲染后的HTML。

#我们可以创建一个Mixin 类来处理JSON 的转换，并将它用于所有的视图。

#该Mixin 提供一个render_to_json_response() 方法，它与 render_to_response() 的参数相同。
# 要使用它，我们只需要将它与TemplateView 组合，并覆盖render_to_response() 来调用render_to_json_response()：
class JSONResponseMixin(object):

    def render_to_json_response(self,context,**response_kwargs):
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )
    def get_data(self,context):
        return context
