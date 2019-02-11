from django.urls import path, re_path
from web import views



urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),

    re_path(r'^run/$', views.UploadFileView.as_view(), name='upload'),
    re_path(r'^document/delete/(?P<pk>\d+)/$', views.delete_document, name='delete_document'),


]
