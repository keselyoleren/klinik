# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from config.choice import DAY_CODE
from django.views.generic import TemplateView
from config.permis import IsAuthenticated, IsAuthenticated
from django.db.models import Count

from master_data.form.jadwal_form import JadwalTenagaMedisForm
from master_data.models import JadwalTenagaMedis

class JadwalTenagaMedisListView(IsAuthenticated, ListView):
    model = JadwalTenagaMedis
    template_name = 'jadwal_tenage_medis/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Jadwal Tenaga Medis'
        nama_list = JadwalTenagaMedis.objects.values('tenaga_medis').annotate(count=Count('tenaga_medis'))
        unique_jadwal_list = []
        for jadwal in nama_list:
            jadwal_obj = JadwalTenagaMedis.objects.filter(tenaga_medis=jadwal['tenaga_medis']).first()
            unique_jadwal_list.append(jadwal_obj)
        context['header_title'] = 'List jadwal Tenaga Medis'
        context['list_jadwal'] = unique_jadwal_list
        context['btn_add'] = True
        context['is_list'] = True
        context['create_url'] = reverse_lazy('jadwal-create')
        return context

class JadwalTenagaMedisDetailView(IsAuthenticated, ListView):
    model = JadwalTenagaMedis
    template_name = 'jadwal_tenage_medis/list.html'
    context_object_name = 'list_jadwal'
    
    def get_queryset(self):
        jadwal = JadwalTenagaMedis.objects.filter(id=self.kwargs['pk']).first()
        return super().get_queryset().filter(tenaga_medis=jadwal.tenaga_medis)

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jadwal = JadwalTenagaMedis.objects.filter(id=self.kwargs['pk']).first()
        context['header'] = f'Jadwal {jadwal.tenaga_medis}'
        context['header_title'] = f'List jadwal {jadwal.tenaga_medis}'
        context['btn_add'] = True
        context['is_list'] = False
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