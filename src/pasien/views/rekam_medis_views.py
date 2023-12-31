# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusRawatJalan
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.form.rekam_medis_form import RekamMedisForm
from pasien.models import RawatJalan, Pasien, RekamMedis
from pasien.form.rawat_jalan_form import RawatJalanForm


class ListRawatJalanView(IsAuthenticated, ListView):
    model = RawatJalan
    template_name = 'rekam_medis/list_pasien.html'
    context_object_name = 'list_rawat_jalan'
    
    def get_queryset(self):
        return super().get_queryset().filter(status=StatusRawatJalan.REGISTRASI)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'List Pasien Rawat Jalan'
        context['header_title'] = 'List Pasien  Rawat Jalan'
        return context


class RekamMedisListView(IsAuthenticated, ListView):
    model = RekamMedis
    template_name = 'rekam_medis/list.html'
    context_object_name = 'list_rekam_medis'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rekam Medis'
        context['header_title'] = 'List Rekam Medis'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('rekam_medis-create')
        return context

class RekamMedisCreateView(IsAuthenticated, CreateView):
    model = RekamMedis
    template_name = 'component/form.html'
    form_class = RekamMedisForm
    success_url = reverse_lazy('rekam_medis-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rekam Medis'
        context['header_title'] = 'Tambah Rekam Medis'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class RekamMedisUpdateView(IsAuthenticated, UpdateView):
    model = RekamMedis
    template_name = 'component/form.html'
    form_class = RekamMedisForm
    success_url = reverse_lazy('rekam_medis-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'RekamMedis'
        context['header_title'] = 'Edit Rekam Medis'
        return context

class RekamMedisDeleteView(IsAuthenticated, DeleteView):
    model = RekamMedis
    template_name = 'component/delete.html'
    success_url = reverse_lazy('relam_medis-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rekam Medis'
        context['header_title'] = 'Delete Rekam Medis'
        return context

