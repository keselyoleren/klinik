# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
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


class DownloadSuratRapidAntigen(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratRapidAntigen
    template_name = 'surat/Rapid/download.html'
    context_object_name = 'list_rapid'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Mengetahui',
                'title': 'SURAT KETERANGAN COVID-19 '
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Rapid - {self.get_object().pasien.full_name}'
        )

