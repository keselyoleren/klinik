# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser
from config.permis import IsAuthenticated, IsPuskeswan
from master_data.form.tenaga_medis_form import TenagaMedisForm

from master_data.models import TenagaMedis



class TenagaMedisListView(IsPuskeswan, ListView):
    model = TenagaMedis
    template_name = 'tenage_medis/list.html'
    context_object_name = 'list_tenaga_medis'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Tenaga Medis'
        context['header_title'] = 'List Tenaga Medis'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('tenaga_medis-create')
        return context

class TenagaMedisCreateView(IsPuskeswan, CreateView):
    model = TenagaMedis
    template_name = 'component/form.html'
    form_class = TenagaMedisForm
    success_url = reverse_lazy('tenaga_medis-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Tenaga Medis'
        context['header_title'] = 'Tambah Tenaga Medis'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class TenagaMedisUpdateView(IsPuskeswan, UpdateView):
    model = TenagaMedis
    template_name = 'component/form.html'
    form_class = TenagaMedisForm
    success_url = reverse_lazy('tenaga_medis-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Tenaga Medis'
        context['header_title'] = 'Edit Tenaga Medis'
        return context

class TenagaMedisDeleteView(IsPuskeswan, DeleteView):
    model = TenagaMedis
    template_name = 'component/delete.html'
    success_url = reverse_lazy('tenaga_medis-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Tenaga Medis'
        context['header_title'] = 'Delete Tenaga Medis'
        return context
