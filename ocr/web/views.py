from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (View,TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from web.forms import DocumentForm
import urllib.parse
import time
from django.http import HttpResponse, Http404, JsonResponse
from .models import Document

class IndexView(TemplateView):
    template_name = 'index.html'


class UploadFileView(View):
    def get(self, request):
        document_list = Document.objects.all()
        return render(self.request, 'upload_file.html', {'documents': document_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = DocumentForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            document = form.save()
            data = {'is_valid': True, 'name': document.file.name, 'url': document.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
