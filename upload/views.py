# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .forms import UploadFileForm,FileFieldForm

# Create your views here.
def handle_uploaded_file(f):
    with open('some/file/name.txt','wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST,request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect(reverse('base_view:thanks'))
#     else:
#         form = UploadFileForm()
#     return render(request,'upload/upload.html',{'form':form})

class UploadFormView(FormView):
    form_class = UploadFileForm
    template_name = 'upload/upload.html'
    success_url = '/base_view/thanks/'
    def form_valid(self, form):
        handle_uploaded_file(self.request.FILES['file'])

# Uploading multiple files¶
#
# If you want to upload multiple files using one form field, set the multiple HTML attribute of field’s widget:
class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload/upload.html'
    success_url = '/base_view/thanks/'
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if files:
            print('aaaaaaaaaaa')
        if form.is_valid():
            for f in files:
                pass
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

