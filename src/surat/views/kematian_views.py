# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
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


class DownloadSuratKematian(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratKematian
    template_name = 'surat/kematian/download.html'
    context_object_name = 'list_kematian'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Mengetahui,',
                'title': 'Surat Kemation'
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Kemation - {self.get_object().pasien.full_name}'
        )

