# myapp/views.py
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


class DownloadSuratPerintahTugas(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratPerintahTugas
    template_name = 'surat/tugas/download.html'
    context_object_name = 'list_tugas'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Pimpinan Klinik Refa Pratama',
                'title': 'SURAT PERINTAH TUGAS '
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Tugas - {self.get_object().tenaga_medis.nama}'
        )

