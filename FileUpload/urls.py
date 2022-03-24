from FileUpload import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^api/upload$', views.fileupload_list),
    re_path(r'^api/files/(?P<pk>[0-9]+)$', views.fileupload_detail),
]
