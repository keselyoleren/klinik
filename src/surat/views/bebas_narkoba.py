# myapp/views.py
from datetime import datetime
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.timezone import localtime

from config.documents import GoogleDocumentProvider
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.models import Pasien
from surat.form.surat_form import GenerateSuratBebasNarkobaForm, SuratBebasNarkoba, SuratBebasNarkobaForm
from surat.models import SuratBebasNarkoba


class SuratBebasNarkobaListView(IsAuthenticated, ListView):
    model = SuratBebasNarkoba
    template_name = 'surat/bebas_narkoba/list.html'
    context_object_name = 'list_bebas_narkoba'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Bebeas Narkoba'
        context['header_title'] = 'List Surat Bebeas Narkoba'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('narkoba-create')
        return context

class SuratBebasNarkobaCreateView(IsAuthenticated, CreateView):
    model = SuratBebasNarkoba
    template_name = 'component/form.html'
    form_class = SuratBebasNarkobaForm
    success_url = reverse_lazy('narkoba-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratBebasNarkobaUpdateView(IsAuthenticated, UpdateView):
    model = SuratBebasNarkoba
    template_name = 'component/form.html'
    form_class = SuratBebasNarkobaForm
    success_url = reverse_lazy('narkoba-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'SuratBebasNarkoba'
        context['header_title'] = 'Edit SuratBebasNarkoba'
        return context

class SuratBebasNarkobaDeleteView(IsAuthenticated, DeleteView):
    model = SuratBebasNarkoba
    template_name = 'component/delete.html'
    success_url = reverse_lazy('narkoba-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Bebeas Narkoba'
        context['header_title'] = 'Delete Surat Bebeas Narkoba'
        return context


class DownloadSuratBebasNarkoba(IsAuthenticated, DetailView):
    model = SuratBebasNarkoba
    template_name = 'surat/bebas_narkoba/download.html'
    context_object_name = 'list_bebas_narkoba'
    
    def get(self, request, *args, **kwargs):
        document_id = '1q7V1wYTGRjr6PnCLFssaQaIH2h9baIwDguXgj9q5Wv8'
        created_at_local = localtime(self.get_object().created_at)
        params = {
            'item.tenaga_medis.nama': self.get_object().tenaga_medis.nama,
            'item.tenaga_medis.no_str': self.get_object().tenaga_medis.no_str,
            'item.tenaga_medis.jabatan': self.get_object().tenaga_medis.jabatan,
            'item.tenaga_medis.alamat': self.get_object().tenaga_medis.alamat,
            'item.pasien.full_name': self.get_object().pasien.full_name,
            'item.pasien.tanggal_lahir': self.get_object().pasien.tanggal_lahir,
            'item.pasien.jenis_kelamin': self.get_object().pasien.jenis_kelamin,
            'item.pasien.pekerjaan': self.get_object().pasien.pekerjaan,
            'item.pasien.alamat': self.get_object().pasien.alamat,
            'item.aphetamin': self.get_object().aphetamin,
            'item.methamphetamine': self.get_object().methamphetamine,
            'item.thc': self.get_object().thc,
            'item.mor': self.get_object().mor,
            'created_at': created_at_local.strftime('%d %B %Y')
        }
        file_name = f'Surat Bebeas Narkoba - {self.get_object().pasien} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name)
        proses_document =  document.process_document()
        return document.download_google_docs_as_pdf(proses_document)

class SuratBebasNarkobaGenerateView(IsAuthenticated, CreateView):
    model = SuratBebasNarkoba
    template_name = 'component/form.html'
    generate_template_name = 'surat/bebas_narkoba/download.html'
    form_class = GenerateSuratBebasNarkobaForm
    success_url = reverse_lazy('narkoba-list')

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Bebas Narkoba'
        context['header_title'] = 'Tambah Bebas Narkoba'
        return context

    def get_pasien(self):
        return Pasien.objects.get(id=self.kwargs['pasien_id'])
    
    def form_valid(self, form):
        form.instance.pasien = self.get_pasien()
        form.save()
        super().form_valid(form)
        return self.generate_document()
    
    def generate_document(self):
        document_id = '1q7V1wYTGRjr6PnCLFssaQaIH2h9baIwDguXgj9q5Wv8'
        params = self.object
        file_name = 'document format'
        return GoogleDocumentProvider(document_id, params, file_name).process_document()
        # return self.render_to_pdf(
        #     {
        #         'item': self.object,
        #         'ttd_keterangan':'Mengetahui',
        #         'title': 'Surat Bebeas Narkoba',
        #         'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
        #     },
        #     self.generate_template_name,
        #     '/css/pdf.css',
        #     f'Surat Bebeas Narkoba - {self.object.pasien}'
        # )
