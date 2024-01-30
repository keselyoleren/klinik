# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from surat.form.surat_form import SuratPenolakanForm
from surat.models import SuratPenolakan


class SuratPenolakanListView(IsAuthenticated, ListView):
    model = SuratPenolakan
    template_name = 'surat/penolakan/list.html'
    context_object_name = 'list_penolakan'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Penolakan Rujukan'
        context['header_title'] = 'List Surat Penolakan Rujukan'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('penolakan-create')
        return context

class SuratPenolakanCreateView(IsAuthenticated, CreateView):
    model = SuratPenolakan
    template_name = 'component/form.html'
    form_class = SuratPenolakanForm
    success_url = reverse_lazy('penolakan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratPenolakanUpdateView(IsAuthenticated, UpdateView):
    model = SuratPenolakan
    template_name = 'component/form.html'
    form_class = SuratPenolakanForm
    success_url = reverse_lazy('penolakan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Penolakan'
        context['header_title'] = 'Edit Surat Penolakan'
        return context

class SuratPenolakanDeleteView(IsAuthenticated, DeleteView):
    model = SuratPenolakan
    template_name = 'component/delete.html'
    success_url = reverse_lazy('penolakan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Penolakan Rujukan'
        context['header_title'] = 'Delete Surat Penolakan Rujukan'
        return context


class DownloadSuratPenolakan(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratPenolakan
    template_name = 'surat/penolakan/download.html'
    context_object_name = 'list_penolakan'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Mengetahui',
                'title': 'Surat Penolakan Rujukan',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Penolakan Rujukan - {self.get_object().pasien}'
        )

