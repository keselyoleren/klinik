# myapp/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.biaya_form import RincianBiayaForm
from pasien.models import  RawatInap, RawatJalan, RincianBiaya

from django.db.models import Sum


class RincianBiayaListView(IsAuthenticated, ListView):
    model = RincianBiaya
    template_name = 'biaya/list.html'
    context_object_name = 'list_biaya'

    def get_pasien(self):
        return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_inap_id'])
    
    def get_queryset(self):
        try:
            return super().get_queryset().filter(pasien_rawat_inap=self.get_pasien())
        except Exception:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rincian Biaya'
        context['header_title'] = 'Rincian Biaya'
        context['btn_add'] = True
        context['pasien'] = self.get_pasien().pasien
        context['create_url'] = reverse_lazy('rincian-biaya-create', kwargs={'pasien_rawat_inap_id': self.kwargs['pasien_rawat_inap_id']})
        context['download_url'] = reverse_lazy('rincian-biaya-download', kwargs={'pasien_rawat_inap_id': self.kwargs['pasien_rawat_inap_id']})
        return context


class RincianBiayaCreateView(IsAuthenticated, CreateView):
    model = RincianBiaya
    template_name = 'component/form.html'
    form_class = RincianBiayaForm
    success_url = reverse_lazy('rincian-biaya-list')

    def get_success_url(self) -> str:
        return reverse_lazy('rincian-biaya-list', kwargs={'pasien_rawat_inap_id': self.kwargs['pasien_rawat_inap_id']})

    def get_pasien_rawat_inap(self):
        try:
            return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_inap_id'])
        except Exception:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rincian Biaya'
        context['header_title'] = 'Rincian Biaya'
        context['pasien'] = self.get_pasien_rawat_inap().pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_inap = self.get_pasien_rawat_inap()
        form.save()
        return super().form_valid(form)

class RincianBiayaUpdateView(IsAuthenticated, UpdateView):
    model = RincianBiaya
    template_name = 'component/form.html'
    form_class = RincianBiayaForm


    def get_success_url(self) -> str:
        return reverse_lazy('rincian-biaya-list', kwargs={'pasien_rawat_inap_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rincian Biaya'
        context['header_title'] = 'Edit Rincian Biaya'
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = self.get_object().pasien_rawat_jalan
        form.save()
        return super().form_valid(form)


class RincianBiayaDeleteView(IsAuthenticated, DeleteView):
    model = RincianBiaya
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('rincian-biaya-list', kwargs={'pasien_rawat_inap_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rincian Biaya'
        context['header_title'] = 'Delete Rincian Biaya'
        return context


class DownloadRincianBiaya(IsAuthenticated, GeneratePDF, ListView):
    model = RincianBiaya
    template_name = 'biaya/download.html'
    context_object_name = 'list_biaya'

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
                'list_biaya': self.get_queryset(),
                'pasien':self.get_pasien(),
                "total_harga" : self.get_queryset().aggregate(Sum('harga'))['harga__sum'],
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"

            },
            self.template_name,
            '/css/pdf.css',
            f'Rincian Biaya Pasien {self.get_pasien().pasien.full_name}'
        )

