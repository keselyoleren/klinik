# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from surat.form.surat_form import SuratBebasNarkoba, SuratBebasNarkobaForm
from surat.models import SuratBebasNarkoba


class SuratBebasNarkobaListView(IsAuthenticated, ListView):
    model = SuratBebasNarkoba
    template_name = 'surat/bebas_narkoba/list.html'
    context_object_name = 'list_bebas_narkoba'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Bebeas Narkoba'
        context['header_title'] = 'List Surat Bebeas Narkoba'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('narkoba-create')
        return context

class SuratBebasNarkobaCreateView(IsAuthenticated, CreateView):
    model = SuratBebasNarkoba
    template_name = 'component/form.html'
    form_class = SuratBebasNarkobaForm
    success_url = reverse_lazy('narkoba-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Keterangan Sehat'
        context['header_title'] = 'Tambah Keterangan Sehat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class SuratBebasNarkobaUpdateView(IsAuthenticated, UpdateView):
    model = SuratBebasNarkoba
    template_name = 'component/form.html'
    form_class = SuratBebasNarkobaForm
    success_url = reverse_lazy('narkoba-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'SuratBebasNarkoba'
        context['header_title'] = 'Edit SuratBebasNarkoba'
        return context

class SuratBebasNarkobaDeleteView(IsAuthenticated, DeleteView):
    model = SuratBebasNarkoba
    template_name = 'component/delete.html'
    success_url = reverse_lazy('narkoba-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Surat Bebeas Narkoba'
        context['header_title'] = 'Delete Surat Bebeas Narkoba'
        return context


class DownloadSuratBebasNarkoba(IsAuthenticated, DetailView, GeneratePDF):
    model = SuratBebasNarkoba
    template_name = 'surat/bebas_narkoba/download.html'
    context_object_name = 'list_bebas_narkoba'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'item': self.get_object(),
                'ttd_keterangan':'Mengetahui',
                'title': 'Surat Bebeas Narkoba',
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Surat Bebeas Narkoba - {self.get_object().pasien}'
        )

