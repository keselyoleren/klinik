# myapp/views.py
from django.utils.timezone import localtime
from config.documents import GoogleDocumentProvider
from config.templatetags.tags import conv_month_to_roman
from datetime import datetime

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.models import Pasien
from surat.form.surat_form import GenerateKetarangaSehatForm, KetarangaSehatForm
from surat.models import KeteranganSehat


class KeteranganSehatListView(IsAuthenticated, ListView):
    model = KeteranganSehat
    template_name = 'surat/keterangan_Sehat/list.html'
    context_object_name = 'list_keterangan_sehat'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keteragan Sehat'
        context['header_title'] = 'List Keteragan Sehat'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('keterangan-sehat-create')
        return context

class KeteranganSehatCreateView(IsAuthenticated, CreateView):
    model = KeteranganSehat
    template_name = 'component/form.html'
    form_class = KetarangaSehatForm
    success_url = reverse_lazy('keterangan-sehat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class KeteranganSehatUpdateView(IsAuthenticated, UpdateView):
    model = KeteranganSehat
    template_name = 'component/form.html'
    form_class = KetarangaSehatForm
    success_url = reverse_lazy('keterangan-sehat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'KeteranganSehat'
        context['header_title'] = 'Edit KeteranganSehat'
        return context

class KeteranganSehatDeleteView(IsAuthenticated, DeleteView):
    model = KeteranganSehat
    template_name = 'component/delete.html'
    success_url = reverse_lazy('keterangan-sehat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keteragan Sehat'
        context['header_title'] = 'Delete Keteragan Sehat'
        return context


class DownloadKeteranganSehat(IsAuthenticated, DetailView):
    model = KeteranganSehat
    template_name = 'surat/keterangan_sehat/download.html'
    context_object_name = 'list_keterangan_sehat'
    
    def get(self, request, *args, **kwargs):
        document_id = '1j_TfJeVde6NrVi7tu-TxPJLdn1-YtAcQBwlT8ZFRfu4'
        created_at_local = localtime(self.get_object().created_at)
        month_only = created_at_local.strftime('%m')
        year_only = created_at_local.strftime('%Y')


        # tgl_lahir = localtime(self.get_object().pasien.tanggal_lahir)
        params = {            
            'created_at': created_at_local.strftime('%Y-%m-%d'), #created_at_local.strftime('%d %B %Y')
            'nama-pasien': self.get_object().pasien.full_name,
            'tgl-lahir': self.get_object().pasien.tanggal_lahir,
            'jenis-kelamin': self.get_object().pasien.jenis_kelamin,
            'pekerjaan': self.get_object().pasien.pekerjaan,
            'alamat': self.get_object().pasien.alamat,
            'nik': self.get_object().pasien.nik,
            'tempat_lahir': self.get_object().pasien.tempat_lahir,
            'agama': self.get_object().pasien.agama,

            'tb': self.get_object().tb,
            'bb': self.get_object().bb,
            'suhu_tubuh': self.get_object().suhu_tubuh,
            'gol_darah': self.get_object().golongan_darah,
            'buta_warna': self.get_object().tes_buta_warna,
            'keperluan': self.get_object().keperluan,

            'no': self.get_object().no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Surat Keterangan Sakit - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)


class KeteranganSehatGenerateView(IsAuthenticated, CreateView, GeneratePDF):
    model = KeteranganSehat
    template_name = 'component/form.html'
    generate_template_name = 'surat/keterangan_sehat/download.html'
    form_class = GenerateKetarangaSehatForm
    success_url = reverse_lazy('keterangan-sehat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def get_pasien(self):
        return Pasien.objects.get(id=self.kwargs['pasien_id'])


    def form_valid(self, form):
        form.instance.pasien = self.get_pasien()
        form.save()
        super().form_valid(form)
        return self.render_pdf()

    def render_pdf(self):
        document_id = '1j_TfJeVde6NrVi7tu-TxPJLdn1-YtAcQBwlT8ZFRfu4'
        created_at_local = localtime(self.object.created_at)
        month_only = created_at_local.strftime('%m')
        year_only = created_at_local.strftime('%Y')


        # tgl_lahir = localtime(self.get_object().pasien.tanggal_lahir)
        params = {            
            'created_at': created_at_local.strftime('%Y-%m-%d'), #created_at_local.strftime('%d %B %Y')
            'nama-pasien': self.object.pasien.full_name,
            'tgl-lahir': self.object.pasien.tanggal_lahir,
            'jenis-kelamin': self.object.pasien.jenis_kelamin,
            'pekerjaan': self.object.pasien.pekerjaan,
            'alamat': self.object.pasien.alamat,
            'nik': self.object.pasien.nik,
            'tempat_lahir': self.object.pasien.tempat_lahir,
            'agama': self.object.pasien.agama,

            'tb': self.object.tb,
            'bb': self.object.bb,
            'suhu_tubuh': self.object.suhu_tubuh,
            'gol_darah': self.object.golongan_darah,
            'buta_warna': self.object.tes_buta_warna,
            'keperluan': self.object.keperluan,

            'no': self.object.no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Surat Keterangan Sakit - {self.object} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)
