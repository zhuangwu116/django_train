"""django11_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from djangtestdemo import views
from datetime import datetime
import django.contrib.auth.views
import vsdemo.forms
import vsdemo.views
admin.autodiscover()
urlpatterns = [
    url(r'^addindex$',views.addindex,name='addindex'),
    url(r'^getmenu$',views.getmenu,name='getmenu'),
    url(r'^addmenu$', views.addmenu, name='addmenu'),
    url(r'^menuindex$', views.menuindex, name='menuindex'),
    url(r'^postlist$',views.getpostlist,name='postlist'),
    url(r'^testform$', views.test_form, name='test_form'),
    url(r'^index$',views.index,name='indext'),
    url(r'^post_list$',views.post_list,name='post_list'),
    url(r'^video-(?P<classification_id>(\d+))-(?P<level_id>(\d+)).html$', views.video,name='video'),
    url(r'^comments/(?:page-(?P<page_number>\d+)/)?$', views.page,name='page'),


    url(r'^',include('vsdemo.urls',namespace='vsdemo')),
    url(r'^contact$',vsdemo.views.contact,name='contact'),
    url(r'^about',vsdemo.views.about,name='about'),
    url(r'^seed',vsdemo.views.seed,name='seed'),
    url(r'^login/$',
        django.contrib.auth.views.login,{
        'template_name':'vsdemo/login.html',
        'authentication_form':vsdemo.forms.BootstrapAuthenticationForm,
        'extra_context':{
            'title':'Log in',
            'year':datetime.now().year,
        }
    },name='login'),
    url(r'logout$',django.contrib.auth.views.logout,{
        'next_page':'/',
    },name='logout'),


    url(r'^base_view/',include('base_view.urls',namespace='base_view')),
    url(r'^admin/', admin.site.urls),
]
