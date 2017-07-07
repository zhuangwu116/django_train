import vsdemo.views
from django.conf.urls import url
from vsdemo.models import Poll
import vsdemo.views
urlpatterns=[
    url(r'^$',
        vsdemo.views.PollListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='vsdemo/index.html',),
        name='home'),
    url(r'^(?P<pk>\d+)/$',
        vsdemo.views.PollDetailView.as_view(
            template_name='vsdemo/details.html'),
         name='detail'),
    url(r'^(?P<pk>\d+)/results/$',
        vsdemo.views.PollResultsView.as_view(
            template_name='vsdemo/results.html'),
        name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$',vsdemo.views.vote,name='vote'),
    url(r'^(?P<poll_id>\d+)/vote/$',vsdemo.views.vote,name='vote')
]