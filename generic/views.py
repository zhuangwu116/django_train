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
        response = super(AjaxableResponseMixin,self).form_invalid(form)
        if self.request.is_ajax():
            data={
                'pk':self.object.pk
            }
            return JsonResponse(data)
        else:
            return response