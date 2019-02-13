from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (View,TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from web.forms import DocumentForm
import urllib.parse
import time
from django.http import HttpResponse, Http404, JsonResponse
from .models import Document
import subprocess


class IndexView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'


class UploadFileView(View):
    def get(self, request):
        document_list = Document.objects.all()
        return render(self.request, 'upload_file.html', {'documents': document_list})

    def post(self, request):
        form = DocumentForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            document = form.save()
            data = {'is_valid': True, 'name': document.file.name, 'url': document.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def delete_document(request, pk):
    try:
        Document.objects.get(pk=pk).delete()
    except Document.DoesNotExist:
        pass
    document_list = Document.objects.all()
    return render(request, 'upload_file.html', {'documents': document_list})

def convert_document(request, pk):
    document = Document.objects.get(pk=pk)

    print(document.file.url)
    print(30*'-')
    command = 'tesseract ' + document.file.path + ' media/documents/output -l eng'
    print(command)
    print(30*'-')
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    print(output)
    print(error)

    with open('media/documents/output.txt', 'r') as myfile:
        data=myfile.read().replace('\n', '<br />')

    document.converted_text = data
    document.save()

    document_list = Document.objects.all()

    return render(request, 'upload_file.html', {'documents': document_list})

def modal_show(request, operation):
    print(operation)
    if 'lookdata' in operation:
        document_pk = operation.split('-')
        document = Document.objects.get(pk=document_pk[1])

        context = {'return_data': document.converted_text, }
        print('no problem')
        return render(request, 'showdata.html', context)
