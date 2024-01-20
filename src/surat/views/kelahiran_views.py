# myapp/views.py
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


class DownloadSuratKelahiran(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratKelahiran
    template_name = 'surat/kelahiran/download.html'
    context_object_name = 'list_kelahiran'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Mengetahui',
                'title': 'Surat Kelahiran',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Kelahiran - {self.get_object().nama_bayi}'
        )

