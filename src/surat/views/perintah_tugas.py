# myapp/views.py
from django.utils.timezone import localtime
from config.documents import GoogleDocumentProvider
from config.templatetags.tags import conv_month_to_roman
from datetime import datetime

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from surat.form.surat_form import SuratPerintahTugas, SuratPerintahTugasForm
from surat.models import SuratPerintahTugas


class SuratPerintahTugasListView(IsAuthenticated, ListView):
    model = SuratPerintahTugas
    template_name = 'surat/tugas/list.html'
    context_object_name = 'list_tugas'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Tugas'
        context['header_title'] = 'List Surat Tugas'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('tugas-create')
        return context

class SuratPerintahTugasCreateView(IsAuthenticated, CreateView):
    model = SuratPerintahTugas
    template_name = 'component/form.html'
    form_class = SuratPerintahTugasForm
    success_url = reverse_lazy('tugas-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Tugas'
        context['header_title'] = 'Tambah Surat Tugas'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratPerintahTugasUpdateView(IsAuthenticated, UpdateView):
    model = SuratPerintahTugas
    template_name = 'component/form.html'
    form_class = SuratPerintahTugasForm
    success_url = reverse_lazy('tugas-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Perintah Tugas'
        context['header_title'] = 'Edit Surat Perintah Tugas'
        return context

class SuratPerintahTugasDeleteView(IsAuthenticated, DeleteView):
    model = SuratPerintahTugas
    template_name = 'component/delete.html'
    success_url = reverse_lazy('tugas-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Tugas'
        context['header_title'] = 'Delete Surat Tugas'
        return context


class DownloadSuratPerintahTugas(IsAuthenticated, DetailView):
    model = SuratPerintahTugas
    template_name = 'surat/tugas/download.html'
    context_object_name = 'list_tugas'
    
    def get(self, request, *args, **kwargs):
        document_id = '1zcVKz2XstKfRNBCzyQMdXnEmnymVCJs9bM8DRdJddSs'
        created_at_local = localtime(self.get_object().created_at)
        month_only = created_at_local.strftime('%m')
        year_only = created_at_local.strftime('%Y')
        params = {            
            'created_at': created_at_local.strftime('%Y-%m-%d'), #created_at_local.strftime('%d %B %Y')
            'dasar': self.get_object().dasar,
            'tujuan': self.get_object().tujuan,

            'nama': self.get_object().tenaga_medis.nama,
            'jabatan':self.get_object().tenaga_medis.jabatan,
            
            'no': self.get_object().no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Surat Kelahiran - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)

