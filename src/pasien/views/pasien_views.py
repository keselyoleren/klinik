# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser
from config.permis import IsAuthenticated, IsPuskeswan
from pasien.models import Pasien
from pasien.form.pasien_form import PasienForm


class PasienListView(IsPuskeswan, ListView):
    model = Pasien
    template_name = 'pasien/list.html'
    context_object_name = 'list_pasien'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien'
        context['header_title'] = 'List Pasien'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('pasien-create')
        return context

class PasienCreateView(IsPuskeswan, CreateView):
    model = Pasien
    template_name = 'component/form.html'
    form_class = PasienForm
    success_url = reverse_lazy('pasien-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien'
        context['header_title'] = 'Tambah Pasien'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class PasienUpdateView(IsPuskeswan, UpdateView):
    model = Pasien
    template_name = 'component/form.html'
    form_class = PasienForm
    success_url = reverse_lazy('pasien-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien'
        context['header_title'] = 'Edit Pasien'
        return context

class PasienDeleteView(IsPuskeswan, DeleteView):
    model = Pasien
    template_name = 'component/delete.html'
    success_url = reverse_lazy('pasien-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien'
        context['header_title'] = 'Delete Pasien'
        return context
