from django.urls import re_path
from CourseTables import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^courses$', views.courseApi),
    re_path(r'^courses/([0-9]+)$', views.courseApi),
    re_path(r'^requests$', views.requestAPI),
    re_path(r'^requests/([0-9]+)$', views.requestAPI),
]