# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusPasien
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.catatan_terintegrasi_form import CatanTerintegrasiForm

from pasien.models import  Pasien, RawatInap, RawatJalan, CatatanTerIntegrasi

class CatanTerintegrasiListView(IsAuthenticated, ListView):
    model = CatatanTerIntegrasi
    template_name = 'catatan_terintegrasi/list.html'
    context_object_name = 'list_integrasi'

    def get_pasien(self):
        try:
            return RawatJalan.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])
        except Exception:
            return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])
    
    def get_queryset(self):
        try:
            try:
                return super().get_queryset().filter(pasien_rawat_jalan=self.get_pasien())
            except Exception:
                return super().get_queryset().filter(pasien_rawat_inap=self.get_pasien())
        except Exception:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Catatan Terintegrasi'
        context['header_title'] = 'Catatan Terintegrasi'
        context['btn_add'] = True
        context['pasien'] = self.get_pasien().pasien
        context['create_url'] = reverse_lazy('catatan-terintegrasi-create', kwargs={'pasien_rawat_jalan_id': self.kwargs['pasien_rawat_jalan_id']})
        context['download_url'] = reverse_lazy('catatan-terintegrasi-download', kwargs={'pasien_rawat_jalan_id': self.kwargs['pasien_rawat_jalan_id']})
        return context


class CatanTerintegrasiCreateView(IsAuthenticated, CreateView):
    model = CatatanTerIntegrasi
    template_name = 'component/form.html'
    form_class = CatanTerintegrasiForm
    success_url = reverse_lazy('catatan-terintegrasi-list')

    def get_success_url(self) -> str:
        return reverse_lazy('catatan-terintegrasi-list', kwargs={'pasien_rawat_jalan_id': self.kwargs['pasien_rawat_jalan_id']})

    def get_pasien_rawat_jalan(self):
        try:
            return RawatJalan.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])
        except Exception:
            return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Catatan Terintegrasi'
        context['header_title'] = 'Catatan Terintegrasi'
        context['pasien'] = context['pasien'] = self.get_pasien_rawat_jalan().pasien
        return context

    def form_valid(self, form):
        try:
            form.instance.pasien_rawat_jalan = self.get_pasien_rawat_jalan()
        except Exception:
            form.instance.pasien_rawat_inap = self.get_pasien_rawat_jalan()
        form.save()
        return super().form_valid(form)

class CatanTerintegrasiUpdateView(IsAuthenticated, UpdateView):
    model = CatatanTerIntegrasi
    template_name = 'component/form.html'
    form_class = CatanTerintegrasiForm


    def get_success_url(self) -> str:
        return reverse_lazy('catatan-terintegrasi-list', kwargs={'pasien_rawat_jalan_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Catatan Terintegrasi'
        context['header_title'] = 'Edit Catatan Terintegrasi'
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = self.get_object().pasien_rawat_jalan
        form.save()
        return super().form_valid(form)


class CatanTerintegrasiDeleteView(IsAuthenticated, DeleteView):
    model = CatatanTerIntegrasi
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('catatan-terintegrasi-list', kwargs={'pasien_rawat_jalan_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Catatan Terintegrasi'
        context['header_title'] = 'Delete Catatan Terintegrasi'
        return context


class DownloadCatatanTerIntegrasi(IsAuthenticated, GeneratePDF, ListView):
    model = CatatanTerIntegrasi
    template_name = 'catatan_terintegrasi/download.html'
    context_object_name = 'list_integrasi'

    def get_pasien(self):
        try:
            return RawatJalan.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])
        except Exception:
            return RawatInap.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])
    
    def get_queryset(self):
        try:
            return super().get_queryset().filter(pasien_rawat_jalan=self.get_pasien())
        except Exception:
            return super().get_queryset()
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'list_integrasi': self.get_queryset(),
                'pasien':self.get_pasien(),
            },
            self.template_name,
            '/css/pdf.css',
            f'Catatan Terintegrasi Pasien {self.get_pasien().pasien.full_name}'
        )

