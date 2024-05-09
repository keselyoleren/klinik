# myapp/views.py
from config.documents import GoogleDocumentProvider
from datetime import datetime
from django.utils.timezone import localtime

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from config.templatetags.tags import conv_month_to_roman
from surat.form.surat_form import SuratRapidAntigen, SuratRapidAntigenForm
from surat.models import SuratRapidAntigen


class SuratRapidAntigenListView(IsAuthenticated, ListView):
    model = SuratRapidAntigen
    template_name = 'surat/rapid/list.html'
    context_object_name = 'list_rapid'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Rapid'
        context['header_title'] = 'List Surat Rapid'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('rapid-create')
        return context

class SuratRapidAntigenCreateView(IsAuthenticated, CreateView):
    model = SuratRapidAntigen
    template_name = 'component/form.html'
    form_class = SuratRapidAntigenForm
    success_url = reverse_lazy('rapid-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Rapid'
        context['header_title'] = 'Tambah Surat Rapid'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratRapidAntigenUpdateView(IsAuthenticated, UpdateView):
    model = SuratRapidAntigen
    template_name = 'component/form.html'
    form_class = SuratRapidAntigenForm
    success_url = reverse_lazy('rapid-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'SuratRapidAntigen'
        context['header_title'] = 'Edit SuratRapidAntigen'
        return context

class SuratRapidAntigenDeleteView(IsAuthenticated, DeleteView):
    model = SuratRapidAntigen
    template_name = 'component/delete.html'
    success_url = reverse_lazy('rapid-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Rapid'
        context['header_title'] = 'Delete Surat Rapid'
        return context


class DownloadSuratRapidAntigen(IsAuthenticated, DetailView):
    model = SuratRapidAntigen
    template_name = 'surat/Rapid/download.html'
    context_object_name = 'list_rapid'
    
    # def get(self, request, *args, **kwargs):
    #     return self.render_to_pdf(
    #         {
    #             'item': self.get_object(),
    #             'ttd_keterangan':'Mengetahui',
    #             'title': 'SURAT KETERANGAN COVID-19 ',
    #             'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
    #         },
    #         self.template_name,
    #         '/css/pdf.css',
    #         f'Surat Rapid - {self.get_object().pasien.full_name}'
    #     )

    def get(self, request, *args, **kwargs):
        document_id = '1BI6-hwmV_UwvxVy8kut5RLpNewXfpSwcR1tYw8vNpOA'
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
            'hasil': self.get_object().hasil,
            'nilai_rujukan': self.get_object().nilai_rujukan,
            'no': self.get_object().no,
            'romawi':conv_month_to_roman(month_only),
            'tgl-pemeriksaan':created_at_local.strftime('%Y-%m-%d'), #created_at_local.strftime('%d %B %Y')
            'year':year_only

            
        }
        file_name = f'Suat rapid antigen - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)
