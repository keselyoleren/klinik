# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from surat.form.surat_form import KetarangaSehatForm
from surat.models import KeteranganSehat


class KeteranganSehatListView(IsAuthenticated, ListView):
    model = KeteranganSehat
    template_name = 'surat/keterangan_Sehat/list.html'
    context_object_name = 'list_keterangan_sehat'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keteragan Sehat'
        context['header_title'] = 'List Keteragan Sehat'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('keterangan-sehat-create')
        return context

class KeteranganSehatCreateView(IsAuthenticated, CreateView):
    model = KeteranganSehat
    template_name = 'component/form.html'
    form_class = KetarangaSehatForm
    success_url = reverse_lazy('keterangan-sehat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class KeteranganSehatUpdateView(IsAuthenticated, UpdateView):
    model = KeteranganSehat
    template_name = 'component/form.html'
    form_class = KetarangaSehatForm
    success_url = reverse_lazy('keterangan-sehat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'KeteranganSehat'
        context['header_title'] = 'Edit KeteranganSehat'
        return context

class KeteranganSehatDeleteView(IsAuthenticated, DeleteView):
    model = KeteranganSehat
    template_name = 'component/delete.html'
    success_url = reverse_lazy('keterangan-sehat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keteragan Sehat'
        context['header_title'] = 'Delete Keteragan Sehat'
        return context


class DownloadKeteranganSehat(IsAuthenticated, DetailView, GeneratePDF):
    model = KeteranganSehat
    template_name = 'surat/keterangan_sehat/download.html'
    context_object_name = 'list_keterangan_sehat'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Yang Memeriksa',
                'title': 'Surat Keterangan Sehat'
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Keterangan Sehat - {self.get_object().pasien.full_name}'
        )

