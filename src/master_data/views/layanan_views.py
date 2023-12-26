# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser
from config.permis import IsAuthenticated, IsAuthenticated
from master_data.models import Layanan
from master_data.form.layanan_form import LayananForm


class LayananListView(IsAuthenticated, ListView):
    model = Layanan
    template_name = 'layanan/list.html'
    context_object_name = 'list_layanan'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Layanan'
        context['header_title'] = 'List Layanan'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('layanan-create')
        return context

class LayananCreateView(IsAuthenticated, CreateView):
    model = Layanan
    template_name = 'component/form.html'
    form_class = LayananForm
    success_url = reverse_lazy('layanan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Layanan'
        context['header_title'] = 'Tambah Layanan'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class LayananUpdateView(IsAuthenticated, UpdateView):
    model = Layanan
    template_name = 'component/form.html'
    form_class = LayananForm
    success_url = reverse_lazy('layanan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Layanan'
        context['header_title'] = 'Edit Layanan'
        return context

class LayananDeleteView(IsAuthenticated, DeleteView):
    model = Layanan
    template_name = 'component/delete.html'
    success_url = reverse_lazy('layanan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Layanan'
        context['header_title'] = 'Delete Layanan'
        return context
