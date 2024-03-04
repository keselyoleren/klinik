# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
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


class DownloadSuratRujukan(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratRujukan
    template_name = 'surat/rujukan/download.html'
    context_object_name = 'list_rujukan'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Mengetahui,',
                'title': 'Surat Rujukan',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Rujukan - {self.get_object().pasien.full_name}'
        )

class GenerateSuratRujukan(IsAuthenticated, CreateView, GeneratePDF):
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

    def generate_pdf(self):
        return self.render_to_pdf(
            {
                'item': self.object,
                'ttd_keterangan':'Mengetahui,',
                'title': 'Surat Rujukan',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.generate_template_name,
            '/css/pdf.css',
            f'Surat Rujukan - {self.object.pasien.full_name}'
        )