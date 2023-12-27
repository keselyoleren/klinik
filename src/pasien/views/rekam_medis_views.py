# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusRawatJalan
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.models import RawatJalan, Pasien
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
