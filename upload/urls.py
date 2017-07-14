from django.conf.urls import url
import views
urlpatterns=[
    url(r'^',views.UploadFormView.as_view(),name='upload_index'),
]