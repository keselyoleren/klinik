# myapp/views.py
from datetime import datetime
from django.utils.timezone import localtime


from config.documents import GoogleDocumentProvider
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from config.templatetags.tags import conv_month_to_roman
from pasien.models import Pasien
from surat.form.surat_form import GenerateSuratRujukanForm, SuratRujukanForm
from surat.models import SuratRujukan


class SuratRujukanListView(IsAuthenticated, ListView):
    model = SuratRujukan
    template_name = 'surat/rujukan/list.html'
    context_object_name = 'list_rujukan'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Rujukan'
        context['header_title'] = 'List Surat Rujukan'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('rujukan-create')
        return context

class SuratRujukanCreateView(IsAuthenticated, CreateView):
    model = SuratRujukan
    template_name = 'component/form.html'
    form_class = SuratRujukanForm
    success_url = reverse_lazy('rujukan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Rujukan'
        context['header_title'] = 'Tambah Surat Rujukan'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratRujukanUpdateView(IsAuthenticated, UpdateView):
    model = SuratRujukan
    template_name = 'component/form.html'
    form_class = SuratRujukanForm
    success_url = reverse_lazy('rujukan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'SuratRujukan'
        context['header_title'] = 'Edit SuratRujukan'
        return context

class SuratRujukanDeleteView(IsAuthenticated, DeleteView):
    model = SuratRujukan
    template_name = 'component/delete.html'
    success_url = reverse_lazy('rujukan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Rujukan'
        context['header_title'] = 'Delete Surat Rujukan'
        return context


class DownloadSuratRujukan(IsAuthenticated, DetailView):
    model = SuratRujukan
    template_name = 'surat/rujukan/download.html'
    context_object_name = 'list_rujukan'
    
    # def get(self, request, *args, **kwargs):
    #     return self.render_to_pdf(
    #         {
    #             'item': self.get_object(),
    #             'ttd_keterangan':'Mengetahui,',
    #             'title': 'Surat Rujukan',
    #             'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
    #         },
    #         self.template_name,
    #         '/css/pdf.css',
    #         f'Surat Rujukan - {self.get_object().pasien.full_name}'
    #     )

    def get(self, request, *args, **kwargs):
        document_id = '1sIvKhvJfAqYJe2I2ND40foRQM0BG7TH_pr9CiTOr_rg'
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
            'agama': self.get_object().pasien.agama,

            'hasil': self.get_object().keluhan,
            't': self.get_object().t,
            'rr': self.get_object().rr,
            'nadi': self.get_object().nadi,
            'tensi': self.get_object().tensi,
            'hb': self.get_object().hb,
            'kesadaran': self.get_object().kesadaran,
            'diagnosa-sementara': self.get_object().diagnosa_sementara,

            'no': self.get_object().no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Suat rapid antigen - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)


class GenerateSuratRujukan(IsAuthenticated, CreateView):
    model = SuratRujukan
    generate_template_name = 'surat/rujukan/download.html'
    template_name = 'component/form.html'
    form_class = GenerateSuratRujukanForm
    success_url = reverse_lazy('rujukan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Rujukan'
        context['header_title'] = 'Tambah Surat Rujukan'
        return context

    def get_pasien(self):
        return Pasien.objects.get(id=self.kwargs['pasien_id'])
    
    def form_valid(self, form):
        form.instance.pasien = self.get_pasien()
        super().form_valid(form)
        return self.generate_pdf()

    # def generate_pdf(self):
    #     return self.render_to_pdf(
    #         {
    #             'item': self.object,
    #             'ttd_keterangan':'Mengetahui,',
    #             'title': 'Surat Rujukan',
    #             'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
    #         },
    #         self.generate_template_name,
    #         '/css/pdf.css',
    #         f'Surat Rujukan - {self.object.pasien.full_name}'
    #     )
    
    def generate_pdf(self, request, *args, **kwargs):
        document_id = '1sIvKhvJfAqYJe2I2ND40foRQM0BG7TH_pr9CiTOr_rg'
        created_at_local = localtime(self.get_object().created_at)
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
            'agama': self.object.pasien.agama,

            'hasil': self.object.keluhan,
            't': self.object.t,
            'rr': self.object.rr,
            'nadi': self.object.nadi,
            'tensi': self.object.tensi,
            'hb': self.object.hb,
            'kesadaran': self.object.kesadaran,
            'diagnosa-sementara': self.object.diagnosa_sementara,

            'no': self.object.no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Suat rapid antigen - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)
