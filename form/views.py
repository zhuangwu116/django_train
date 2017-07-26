# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import ContactForm
# Create your views here.
def send_mail(request):
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        if forms.is_valid():
            subject = forms.cleaned_data['subject']
            message = forms.cleaned_data['message']
            sender = forms.cleaned_data['sender']
            cc_myself = forms.cleaned_data['cc_myself']
            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)
            send_mail(subject,message,sender,recipients)
    else:
        forms = ContactForm()
    return render(request,'forms/send_mail.html',{"forms":forms})