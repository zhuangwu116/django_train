# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from vsdemo.models import Choice,Poll
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView,DetailView
from os import path
import json
# Create your views here.
class PollListView(ListView):
    model = Poll
    def get_context_data(self, **kwargs):
        context=super(PollListView,self).get_context_data(**kwargs)
        context['title']='Polls'
        context['year']=datetime.now().year
        return context
class PollDetailView(DetailView):
    model = Poll
    def get_context_data(self, **kwargs):
        context=super(PollDetailView,self).get_context_data(**kwargs)
        context['title']='Poll'
        context['year']=datetime.now().year
        return context
class PollResultsView(DetailView):
    model = Poll
    def get_context_data(self, **kwargs):
        context=super(PollResultsView, self).get_context_data(**kwargs)
        context['title']='Results'
        context['year']=datetime.now().year
        return context
def contact(request):
    assert isinstance(request,HttpRequest)

    return render(request,'vsdemo/contact.html',{
        'title':'Contact',
        'message':'Your contact page',
        'year':datetime.now().year,
    })

def about(request):
    assert isinstance(request,HttpRequest)
    return render(request,'vsdemo/about.html',{
        'title':'About',
        'message':'Your application description page.',
        'year':datetime.now().year,
    })

def vote(request,poll_id):
    poll=get_object_or_404(Poll,pk=poll_id)
    try:
        selected_choice=poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'vsdemo/details.html',{
            'title':'Poll',
            'year':datetime.now().year,
            'poll':poll,
            'error_message':'Please make a selection.',
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('vsdemo:results',args=(poll.id)))


@login_required
def seed(request):
    samples_path=path.join(path.dirname(__file__),'samples.json')
    with open(samples_path,'r') as samples_file:
        samples_polls=json.load(samples_file)
        for sample_poll in samples_polls:
            poll=Poll()
            poll.text=sample_poll['text']
            poll.pub_date=timezone.now()
            poll.save()
            for sample_choice in sample_poll['choices']:
                choice=Choice()
                choice.poll=poll
                choice.text=sample_choice
                choice.votes=0
                choice.save()
    return HttpResponseRedirect(reverse('vsdemo:home'))