# myapp/views.py
from datetime import datetime
from django.utils.timezone import localtime
from config.documents import GoogleDocumentProvider

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from config.templatetags.tags import conv_month_to_roman
from surat.form.surat_form import SuratKematianForm

from surat.models import SuratKematian


class SuratKematianListView(IsAuthenticated, ListView):
    model = SuratKematian
    template_name = 'surat/kematian/list.html'
    context_object_name = 'list_kematian'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Kemation'
        context['header_title'] = 'List Surat Kemation'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('kematian-create')
        return context

class SuratKematianCreateView(IsAuthenticated, CreateView):
    model = SuratKematian
    template_name = 'component/form.html'
    form_class = SuratKematianForm
    success_url = reverse_lazy('kematian-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Kemation'
        context['header_title'] = 'Tambah Surat Kemation'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratKematianUpdateView(IsAuthenticated, UpdateView):
    model = SuratKematian
    template_name = 'component/form.html'
    form_class = SuratKematianForm
    success_url = reverse_lazy('kematian-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'SuratKematian'
        context['header_title'] = 'Edit SuratKematian'
        return context

class SuratKematianDeleteView(IsAuthenticated, DeleteView):
    model = SuratKematian
    template_name = 'component/delete.html'
    success_url = reverse_lazy('kematian-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Kemation'
        context['header_title'] = 'Delete Surat Kemation'
        return context


class DownloadSuratKematian(IsAuthenticated, DetailView):
    model = SuratKematian
    template_name = 'surat/kematian/download.html'
    context_object_name = 'list_kematian'
    
    # def get(self, request, *args, **kwargs):
    #     return self.render_to_pdf(
    #         {
    #             'item': self.get_object(),
    #             'ttd_keterangan':'Mengetahui,',
    #             'title': 'Surat Kemation',
    #             'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
    #         },
    #         self.template_name,
    #         '/css/pdf.css',
    #         f'Surat Kemation - {self.get_object().pasien.full_name}'
    #     )

    def get(self, request, *args, **kwargs):
        document_id = '10toTgdO_BwIlazUD6M-iQ_nexwy9JBHGP2z-7z19DBM'
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

            'tempat_kematian': self.get_object().tempat_kematian,
            'tgl_kematian': self.get_object().tanggal_kematian,
            'sebab_kematian': self.get_object().sebab_kematian,

            'no': self.get_object().no,
            'romawi':conv_month_to_roman(month_only),
            'year':year_only

            
        }
        file_name = f'Surat Kematian - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)
