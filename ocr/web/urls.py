from django.urls import path, re_path
from web import views



urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
]
