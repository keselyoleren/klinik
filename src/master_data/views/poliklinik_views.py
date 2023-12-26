# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser
from config.permis import IsAuthenticated, IsPuskeswan
from master_data.form.poliklinik_form import PoliKlinikForm
from master_data.models import PoliKlinik



class PoliKlinikListView(IsPuskeswan, ListView):
    model = PoliKlinik
    template_name = 'poliklinik/list.html'
    context_object_name = 'list_poliklinik'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Poli Klinik'
        context['header_title'] = 'List Poli Klinik'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('poliklinik-create')
        return context

class PoliKlinikCreateView(IsPuskeswan, CreateView):
    model = PoliKlinik
    template_name = 'component/form.html'
    form_class = PoliKlinikForm
    success_url = reverse_lazy('poliklinik-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Poli Klinik'
        context['header_title'] = 'Tambah Poli Klinik'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class PoliKlinikUpdateView(IsPuskeswan, UpdateView):
    model = PoliKlinik
    template_name = 'component/form.html'
    form_class = PoliKlinikForm
    success_url = reverse_lazy('poliklinik-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Poli Klinik'
        context['header_title'] = 'Edit Poli Klinik'
        return context

class PoliKlinikDeleteView(IsPuskeswan, DeleteView):
    model = PoliKlinik
    template_name = 'component/delete.html'
    success_url = reverse_lazy('poliklinik-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Poli Klinik'
        context['header_title'] = 'Delete Poli Klinik'
        return context
