# myapp/views.py
from django.utils.timezone import localtime
from config.documents import GoogleDocumentProvider
from config.templatetags.tags import conv_month_to_roman
from datetime import datetime

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from surat.form.surat_form import SuratKelahiran, SuratKelahiranForm
from surat.models import SuratKelahiran


class SuratKelahiranListView(IsAuthenticated, ListView):
    model = SuratKelahiran
    template_name = 'surat/kelahiran/list.html'
    context_object_name = 'list_kelahiran'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Kelahiran'
        context['header_title'] = 'List Surat Kelahiran'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('kelahiran-create')
        return context

class SuratKelahiranCreateView(IsAuthenticated, CreateView):
    model = SuratKelahiran
    template_name = 'component/form.html'
    form_class = SuratKelahiranForm
    success_url = reverse_lazy('kelahiran-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratKelahiranUpdateView(IsAuthenticated, UpdateView):
    model = SuratKelahiran
    template_name = 'component/form.html'
    form_class = SuratKelahiranForm
    success_url = reverse_lazy('kelahiran-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'SuratKelahiran'
        context['header_title'] = 'Edit SuratKelahiran'
        return context

class SuratKelahiranDeleteView(IsAuthenticated, DeleteView):
    model = SuratKelahiran
    template_name = 'component/delete.html'
    success_url = reverse_lazy('kelahiran-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Kelahiran'
        context['header_title'] = 'Delete Surat Kelahiran'
        return context


class DownloadSuratKelahiran(IsAuthenticated, DetailView):
    model = SuratKelahiran
    template_name = 'surat/kelahiran/download.html'
    context_object_name = 'list_kelahiran'
    
    def get(self, request, *args, **kwargs):
        document_id = '14YxnN1qjoARMpXBfKRcWKEo0CTzc9gqseNw7W_kb59k'
        created_at_local = localtime(self.get_object().created_at)
        month_only = created_at_local.strftime('%m')
        year_only = created_at_local.strftime('%Y')
        params = {            
            'created_at': created_at_local.strftime('%Y-%m-%d'), #created_at_local.strftime('%d %B %Y')
            
            'nama_bayi': self.get_object().nama_bayi,
            'jenis_kelamin': self.get_object().jenis_kelamin,
            'panjang_badan': self.get_object().panjang_badan,
            'berat_badan': self.get_object().berat_badan,
            'hari': self.get_object().hari,
            'tgl_lahir': self.get_object().tanggal_lahir,
            'jam': self.get_object().jam,
            'tempat': self.get_object().tempat,
            'nama_ayah': self.get_object().nama_ayah,
            'nama_ibu': self.get_object().nama_ibu,
            'alamat': self.get_object().alamat,

            'no': self.get_object().no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Surat Kelahiran - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)

