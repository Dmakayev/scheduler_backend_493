from django.urls import re_path
from FacultyNames import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^FacultyNames$', views.facultyApi),
    re_path(r'^FacultyNames/([0-9]+)$', views.facultyApi)
]