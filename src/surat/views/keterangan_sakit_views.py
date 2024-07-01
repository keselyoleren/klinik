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
from surat.form.surat_form import GenerateKetarangaSakitForm, KetarangaSakitForm
from surat.models import KeteraganSakit


class KeteraganSakitListView(IsAuthenticated, ListView):
    model = KeteraganSakit
    template_name = 'surat/keterangan_sakit/list.html'
    context_object_name = 'list_keterangan_sakit'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keteragan Sakit'
        context['header_title'] = 'List Keteragan Sakit'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('keterangan-sakit-create')
        return context

class KeteraganSakitCreateView(IsAuthenticated, CreateView):
    model = KeteraganSakit
    template_name = 'component/form.html'
    form_class = KetarangaSakitForm
    success_url = reverse_lazy('keterangan-sakit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'KeteraganSakit'
        context['header_title'] = 'Tambah KeteraganSakit'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class KeteraganSakitUpdateView(IsAuthenticated, UpdateView):
    model = KeteraganSakit
    template_name = 'component/form.html'
    form_class = KetarangaSakitForm
    success_url = reverse_lazy('keterangan-sakit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'KeteraganSakit'
        context['header_title'] = 'Edit KeteraganSakit'
        return context

class KeteraganSakitDeleteView(IsAuthenticated, DeleteView):
    model = KeteraganSakit
    template_name = 'component/delete.html'
    success_url = reverse_lazy('keterangan-sakit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keteragan Sakit'
        context['header_title'] = 'Delete Keteragan Sakit'
        return context


class DownloadKeteranganSakit(IsAuthenticated, DetailView, GeneratePDF):
    model = KeteraganSakit
    template_name = 'surat/keterangan_sakit/download.html'
    context_object_name = 'list_keterangan_sakit'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Yang Memeriksa',
                'title': 'Surat Keterangan Sakit',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Keterangan Sakit - {self.get_object().pasien.full_name}'
        )
    def get(self, request, *args, **kwargs):
        document_id = '1AhB0VzI70oUs0P1wUbc3lapQMHJjwTociYtoGIVfgz8'
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
            'alamat': self.get_object().pasien.alamat,
            'nik': self.get_object().pasien.nik,
            'tempat_lahir': self.get_object().pasien.tempat_lahir,
            'agama': self.get_object().pasien.agama,

            'diagnosa': self.get_object().diangnosa,
            'start': self.get_object().start,
            'end': self.get_object().end,

            'no': self.get_object().no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Surat Keterangan Sakit - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)


class KeteraganSakitGenerateView(IsAuthenticated, CreateView):
    model = KeteraganSakit
    template_name = 'component/form.html'
    pdf_template_name = 'surat/keterangan_sakit/download.html'
    form_class = GenerateKetarangaSakitForm
    success_url = reverse_lazy('keterangan-sakit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keteragan Sakit'
        context['header_title'] = 'Tambah KeteraganSakit'
        return context
    
    def get_pasien(self):
        return Pasien.objects.get(id=self.kwargs['pasien_id'])

    def form_valid(self, form):
        form.instance.pasien = self.get_pasien()
        super().form_valid(form)
        return self.generate_pdf()
    
    def generate_pdf(self):
        document_id = '1AhB0VzI70oUs0P1wUbc3lapQMHJjwTociYtoGIVfgz8'
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
            'alamat': self.object.pasien.alamat,
            'nik': self.object.pasien.nik,
            'tempat_lahir': self.object.pasien.tempat_lahir,
            'agama': self.object.pasien.agama,

            'diagnosa': self.object.diangnosa,
            'start': self.object.start,
            'end': self.object.end,

            'no': self.object.no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Surat Keterangan Sakit - {self.object} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)
