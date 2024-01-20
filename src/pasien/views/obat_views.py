# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.obat_form import ObatForm


from pasien.models import  RawatInap, RawatJalan, Obat

class ObatListView(IsAuthenticated, ListView):
    model = Obat
    template_name = 'obat/list.html'
    context_object_name = 'list_obat'

    def get_pasien(self):
        return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_inap_id'])
    
    def get_queryset(self):
        try:
            return super().get_queryset().filter(pasien_rawat_inap=self.get_pasien())
        except Exception:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pemakaian Obat'
        context['header_title'] = 'Pemakaian Obat'
        context['btn_add'] = True
        context['pasien'] = self.get_pasien().pasien
        context['create_url'] = reverse_lazy('obat-create', kwargs={'pasien_rawat_inap_id': self.kwargs['pasien_rawat_inap_id']})
        context['download_url'] = reverse_lazy('obat-download', kwargs={'pasien_rawat_inap_id': self.kwargs['pasien_rawat_inap_id']})
        return context


class ObatCreateView(IsAuthenticated, CreateView):
    model = Obat
    template_name = 'component/form.html'
    form_class = ObatForm
    success_url = reverse_lazy('obat-list')

    def get_success_url(self) -> str:
        return reverse_lazy('obat-list', kwargs={'pasien_rawat_inap_id': self.kwargs['pasien_rawat_inap_id']})

    def get_pasien_rawat_inap(self):
        try:
            return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_inap_id'])
        except Exception:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pemakaian Obat'
        context['header_title'] = 'Pemakaian Obat'
        context['pasien'] = self.get_pasien_rawat_inap().pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_inap = self.get_pasien_rawat_inap()
        form.save()
        return super().form_valid(form)

class ObatUpdateView(IsAuthenticated, UpdateView):
    model = Obat
    template_name = 'component/form.html'
    form_class = ObatForm


    def get_success_url(self) -> str:
        return reverse_lazy('obat-list', kwargs={'pasien_rawat_inap_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pemakaian Obat'
        context['header_title'] = 'Edit Pemakaian Obat'
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = self.get_object().pasien_rawat_jalan
        form.save()
        return super().form_valid(form)


class ObatDeleteView(IsAuthenticated, DeleteView):
    model = Obat
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('obat-list', kwargs={'pasien_rawat_inap_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pemakaian Obat'
        context['header_title'] = 'Delete Pemakaian Obat'
        return context


class DownloadObat(IsAuthenticated, GeneratePDF, ListView):
    model = Obat
    template_name = 'obat/download.html'
    context_object_name = 'list_obat'

    def get_pasien(self):
        try:
            return RawatJalan.objects.get(pk=self.kwargs['pasien_rawat_inap_id'])
        except Exception:
            return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_inap_id'])
    
    def get_queryset(self):
        try:
            return super().get_queryset().filter(pasien_rawat_jalan=self.get_pasien())
        except Exception:
            return super().get_queryset()
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'list_obat': self.get_queryset(),
                'pasien':self.get_pasien(),
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Pemakaian Obat Pasien {self.get_pasien().pasien.full_name}'
        )

