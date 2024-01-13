# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusPasien
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.form.rawat_inap import RawatInapForm
from pasien.models import RawatInap, Pasien, RawatInap


class RawatInapListView(IsAuthenticated, ListView):
    model = RawatInap
    template_name = 'rawat_inap/list.html'
    context_object_name = 'list_rawat_inap'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Rawat Inap'
        context['header_title'] = 'List Pasien Rawat Inap'
        context['btn_add'] = True
        
        context['create_url'] = reverse_lazy('rawat_inap-create')
        return context

class RawatInapCreateView(IsAuthenticated, CreateView):
    model = RawatInap
    template_name = 'component/form.html'
    form_class = RawatInapForm
    success_url = reverse_lazy('rawat_inap-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Inap'
        context['header_title'] = 'Tambah Rawat Inap'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class RawatInapUpdateView(IsAuthenticated, UpdateView):
    model = RawatInap
    template_name = 'rawat_inap/detail.html'
    form_class = RawatInapForm
    success_url = reverse_lazy('rawat_inap-list')
    context_object_name = 'rawat_inap'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Inap'
        context['pasien'] = Pasien.objects.get(pk=self.get_object().pasien.id)
        context['header_title'] = 'Edit Rawat Inap'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class RawatInapDeleteView(IsAuthenticated, DeleteView):
    model = RawatInap
    template_name = 'component/delete.html'
    success_url = reverse_lazy('rawat_inap-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Inap'
        context['header_title'] = 'Delete Rawat Inap'
        return context
