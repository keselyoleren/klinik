# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import DAY_CODE, RoleUser
from django.views.generic import TemplateView
from config.permis import IsAuthenticated, IsAuthenticated

from master_data.form.jadwal_form import JadwalTenagaMedisForm
from master_data.models import JadwalTenagaMedis



class JadwalTenagaMedisListView(IsAuthenticated, ListView):
    model = JadwalTenagaMedis
    template_name = 'jadwal_tenage_medis/list.html'
    context_object_name = 'list_jadwal'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Jadwal Tenaga Medis'
        context['header_title'] = 'List jadwal Tenaga Medis'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('jadwal-create')
        return context

class JadwalTenagaMedisCreateView(IsAuthenticated, CreateView):
    model = JadwalTenagaMedis
    template_name = 'component/form.html'
    form_class = JadwalTenagaMedisForm
    success_url = reverse_lazy('jadwal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Jadwal Tenaga Medis'
        context['header_title'] = 'Tambah Tenaga Medis'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class JadwalTenagaMedisUpdateView(IsAuthenticated, UpdateView):
    model = JadwalTenagaMedis
    template_name = 'component/form.html'
    form_class = JadwalTenagaMedisForm
    success_url = reverse_lazy('jadwal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Jadwal Tenaga Medis'
        context['header_title'] = 'Edit Tenaga Medis'
        return context

class JadwalTenagaMedisDeleteView(IsAuthenticated, DeleteView):
    model = JadwalTenagaMedis
    template_name = 'component/delete.html'
    success_url = reverse_lazy('jadwal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Jadwal Tenaga Medis'
        context['header_title'] = 'Delete Tenaga Medis'
        return context



class JadwalView(IsAuthenticated, TemplateView):
    template_name= 'jadwal_tenage_medis/jadwal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Jadwal Tenaga Medis'
        
        context['header_title'] = 'Jadwal Tenaga Medis'
        context['jadwal'] = [
            {
                'title': f"{jadwal.tenaga_medis}",
                'hari': jadwal.hari,
                'code_hari': DAY_CODE.get(jadwal.hari, None),
                'duration': f"{jadwal.jam_mulai.strftime('%H:%M')} - {jadwal.jam_selesai.strftime('%H:%M')}",
                
            } for jadwal in JadwalTenagaMedis.objects.filter(is_active=True)
        ]
        return context