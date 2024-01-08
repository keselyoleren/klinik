# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusPasien
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.form.catatan_terintegrasi_form import CatanTerintegrasiForm

from pasien.models import  Pasien, RawatJalan, RawatJalanTerIntegrasi

class CatanTerintegrasiListView(IsAuthenticated, ListView):
    model = RawatJalanTerIntegrasi
    template_name = 'rawat_jalan/list_catatan_terintegrasi.html'
    context_object_name = 'list_integrasi'

    def get_pasien_rawat_jalan(self):
        try:
            return RawatJalan.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])
        except Exception:
            return None
    
    def get_queryset(self):
        try:
            return super().get_queryset().filter(pasien_rawat_jalan=self.get_pasien_rawat_jalan())
        except Exception:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Catatan Terintegrasi'
        context['header_title'] = 'Catatan Terintegrasi'
        context['btn_add'] = True
        context['pasien'] = self.get_pasien_rawat_jalan().pasien
        context['create_url'] = reverse_lazy('catatan-terintegrasi-create', kwargs={'pasien_rawat_jalan_id': self.kwargs['pasien_rawat_jalan_id']})
        return context


class CatanTerintegrasiCreateView(IsAuthenticated, CreateView):
    model = RawatJalanTerIntegrasi
    template_name = 'component/form.html'
    form_class = CatanTerintegrasiForm
    success_url = reverse_lazy('catatan-terintegrasi-list')

    def get_success_url(self) -> str:
        return reverse_lazy('catatan-terintegrasi-list', kwargs={'pasien_rawat_jalan_id': self.kwargs['pasien_rawat_jalan_id']})

    def get_pasien_rawat_jalan(self):
        try:
            return RawatJalan.objects.get(pk=self.kwargs['pasien_rawat_jalan_id'])
        except Exception:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Catatan Terintegrasi'
        context['header_title'] = 'Catatan Terintegrasi'
        context['pasien'] = context['pasien'] = self.get_pasien_rawat_jalan().pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = self.get_pasien_rawat_jalan()
        form.save()
        return super().form_valid(form)

class CatanTerintegrasiUpdateView(IsAuthenticated, UpdateView):
    model = RawatJalanTerIntegrasi
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
    model = RawatJalanTerIntegrasi
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('catatan-terintegrasi-list', kwargs={'pasien_rawat_jalan_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Catatan Terintegrasi'
        context['header_title'] = 'Delete Catatan Terintegrasi'
        return context
