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
import os

def get_session_key(request):
    print(request.session.session_key)
    if not request.session.exists(request.session.session_key):
        return request.session.create()
    else:
        return request.session.session_key

def get_document_list(request):
    session_key = get_session_key(request)
    return Document.objects.filter(session_key=session_key)


class IndexView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'


class UploadFileView(View):
    def get(self, request):
        session_key = get_session_key(request)
        document_list = get_document_list(request)
        return render(self.request, 'upload_file.html', {'documents': document_list, })

    def post(self, request):
        session_key = get_session_key(request)
        document_list = get_document_list(request)
        form = DocumentForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            document = form.save()
            document.session_key = session_key
            document.save()
            data = {'is_valid': True, 'name': document.file.name, 'url': document.file.url, }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def delete_document(request, pk):
    session_key = get_session_key(request)
    try:
        Document.objects.get(pk=pk,session_key=session_key).delete()
    except Document.DoesNotExist:
        pass
    document_list = get_document_list(request)
    return render(request, 'upload_file.html', {'documents': document_list})

def download_document(request, pk):
    try:
        session_key = get_session_key(request)
        document = Document.objects.get(pk=pk, session_key=session_key)
        lines = document.converted_text.split('<br />')
        file_path = "media/documents/download.txt"
        with open(file_path, "w") as text_file:
            for line in lines:
                text_file.writelines(line + '\n')

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    except:
        document_list = get_document_list(request)
        return render(request, 'upload_file.html', {'documents': document_list})



def convert_document(request, pk, lang):
    session_key = get_session_key(request)

    try:
        document = Document.objects.get(pk=pk, session_key=session_key )

        print(document.file.url)
        print(30*'-')
        command = 'tesseract ' + document.file.path + ' media/documents/output -l ' + lang
        print(command)
        print(30*'-')
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        print(output)
        print(error)

        with open('media/documents/output.txt', 'r') as myfile:
            data=myfile.read().replace('\n', '<br />')

        document.converted_text = data
        document.selected_lang = lang
        document.save()

        document_list = get_document_list(request)

        return render(request, 'upload_file.html', {'documents': document_list})
    except :
        document_list = get_document_list(request)
        return render(request, 'upload_file.html', {'documents': document_list})

def modal_show(request, operation):
    print(operation)
    session_key = get_session_key(request)

    if 'lookdata' in operation:
        document_pk = operation.split('-')
        document = Document.objects.get(pk=document_pk[1],session_key=session_key)

        context = {'return_data': document.converted_text, }
        return render(request, 'showdata.html', context)
    elif 'convertdata' in operation:
        document_pk = operation.split('-')
        return convert_document(request, document_pk[2], document_pk[3])
