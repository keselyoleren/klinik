# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from surat.form.surat_form import SuratPersetujuan, SuratPersetujuanForm
from surat.models import SuratPersetujuan


class SuratPersetujuanListView(IsAuthenticated, ListView):
    model = SuratPersetujuan
    template_name = 'surat/persetujuan/list.html'
    context_object_name = 'list_persetujuan'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Persetujuan Tindakan Medik'
        context['header_title'] = 'List Surat Persetujuan Tindakan Medik'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('persetujuan-create')
        return context

class SuratPersetujuanCreateView(IsAuthenticated, CreateView):
    model = SuratPersetujuan
    template_name = 'component/form.html'
    form_class = SuratPersetujuanForm
    success_url = reverse_lazy('persetujuan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratPersetujuanUpdateView(IsAuthenticated, UpdateView):
    model = SuratPersetujuan
    template_name = 'component/form.html'
    form_class = SuratPersetujuanForm
    success_url = reverse_lazy('persetujuan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'SuratPersetujuan'
        context['header_title'] = 'Edit SuratPersetujuan'
        return context

class SuratPersetujuanDeleteView(IsAuthenticated, DeleteView):
    model = SuratPersetujuan
    template_name = 'component/delete.html'
    success_url = reverse_lazy('persetujuan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Persetujuan Tindakan Medik'
        context['header_title'] = 'Delete Surat Persetujuan Tindakan Medik'
        return context


class DownloadSuratPersetujuan(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratPersetujuan
    template_name = 'surat/persetujuan/download.html'
    context_object_name = 'list_persetujuan'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Mengetahui',
                'title': 'Surat Persetujuan Tindakan Medik',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Persetujuan Tindakan Medik - {self.get_object().pasien}'
        )

