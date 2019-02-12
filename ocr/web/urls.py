from django.urls import path, re_path
from web import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    re_path(r'^$', views.UploadFileView.as_view(), name='upload'),
    re_path(r'^about/$', views.AboutView.as_view(), name='about'),
    re_path(r'^document/delete/(?P<pk>\d+)/$', views.delete_document, name='delete_document'),
    re_path(r'^document/convert/(?P<pk>\d+)/$', views.convert_document, name='convert_document'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
