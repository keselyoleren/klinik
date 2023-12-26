# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.models import RawatJalan, Pasien
from pasien.form.rawat_jalan_form import RawatJalanForm


class RawatJalanListView(IsAuthenticated, ListView):
    model = RawatJalan
    template_name = 'rawat_jalan/list.html'
    context_object_name = 'list_rawat_jalan'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Jalan'
        context['header_title'] = 'List Rawat Jalan'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('rawat_jalan-create')
        return context

class RawatJalanCreateView(IsAuthenticated, CreateView):
    model = RawatJalan
    template_name = 'component/form.html'
    form_class = RawatJalanForm
    success_url = reverse_lazy('rawat_jalan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Jalan'
        context['header_title'] = 'Tambah Rawat Jalan'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class RawatJalanUpdateView(IsAuthenticated, UpdateView):
    model = RawatJalan
    template_name = 'component/form.html'
    form_class = RawatJalanForm
    success_url = reverse_lazy('rawat_jalan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Jalan'
        context['header_title'] = 'Edit Rawat Jalan'
        return context

class RawatJalanDeleteView(IsAuthenticated, DeleteView):
    model = RawatJalan
    template_name = 'component/delete.html'
    success_url = reverse_lazy('rawat_jalan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Jalan'
        context['header_title'] = 'Delete Rawat Jalan'
        return context
