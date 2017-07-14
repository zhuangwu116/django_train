from django.conf.urls import url
import views
urlpatterns=[
    url(r'^',views.UploadFormView.as_view(),name='upload_index'),
    url(r'^filefield', views.FileFieldView.as_view(), name='filefield'),
]