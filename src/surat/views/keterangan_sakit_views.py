# myapp/views.py
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

class KeteraganSakitGenerateView(IsAuthenticated, CreateView, GeneratePDF):
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
        return self.render_to_pdf(
            {
                'item': self.object,
                'ttd_keterangan':'Yang Memeriksa',
                'title': 'Surat Keterangan Sakit',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.pdf_template_name,
            '/css/pdf.css',
            f'Surat Keterangan Sakit - {self.object.pasien.full_name}'
        )