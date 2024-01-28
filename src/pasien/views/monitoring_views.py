# myapp/views.py

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.fisioterapi_form import MonitoringFisoterapiForm


from pasien.models import  Pasien, PasienFisioterapi, RawatInap, RawatJalan, MonitoringFisoterapi

class MonitoringFisoterapiListView(IsAuthenticated, ListView):
    model = MonitoringFisoterapi
    template_name = 'fisio_terapi/monitor.html'
    context_object_name = 'list_fisioterapi'

    def get_pasien_fisioterapi(self):
        return get_object_or_404(PasienFisioterapi, pk=self.kwargs['pasien_id'])
        
    
    def get_queryset(self):
        return super().get_queryset().filter(pasien_fisioterapi=self.get_pasien_fisioterapi())
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Monitoring Fisioterapi'
        context['header_title'] = 'Monitoring Fisioterapi'
        context['btn_add'] = True
        context['pasien'] = self.get_pasien_fisioterapi().pasien
        context['create_url'] = reverse_lazy('monitor-fisioterapi-create', kwargs={'pasien_id': self.kwargs['pasien_id']})
        context['download_url'] = reverse_lazy('monitor-fisioterapi-download', kwargs={'pasien_id': self.kwargs['pasien_id']})
        return context


class MonitoringFisoterapiCreateView(IsAuthenticated, CreateView):
    model = MonitoringFisoterapi
    template_name = 'component/form.html'
    form_class = MonitoringFisoterapiForm
    success_url = reverse_lazy('monitor-fisioterapi-list')

    def get_success_url(self) -> str:
        return reverse_lazy('monitor-fisioterapi-list', kwargs={'pasien_id': self.kwargs['pasien_id']})

    def get_pasien_fisioterapi(self):
        return get_object_or_404(PasienFisioterapi, pk=self.kwargs['pasien_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Monitoring Fisioterapi'
        context['header_title'] = 'Monitoring Fisioterapi'
        context['pasien'] = context['pasien'] = self.get_pasien_fisioterapi().pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_pasien_fisioterapi()
        form.save()
        messages.success(self.request, 'Create data success')
        return super().form_valid(form)

class MonitoringFisoterapiUpdateView(IsAuthenticated, UpdateView):
    model = MonitoringFisoterapi
    template_name = 'component/form.html'
    form_class = MonitoringFisoterapiForm


    def get_success_url(self) -> str:
        return reverse_lazy('monitor-fisioterapi-list', kwargs={'pasien_id': self.get_object().pasien_fisioterapi.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Monitoring Fisioterapi'
        context['header_title'] = 'Edit Monitoring Fisioterapi'
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_object().pasien_fisioterapi
        form.save()
        messages.success(self.request, 'Update data success')
        return super().form_valid(form)


class MonitoringFisoterapiDeleteView(IsAuthenticated, DeleteView):
    model = MonitoringFisoterapi
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('monitor-fisioterapi-list', kwargs={'pasien_id': self.get_object().pasien_fisioterapi.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Monitoring Fisioterapi'
        context['header_title'] = 'Delete Monitoring Fisioterapi'
        return context


class DownloadMonitoringFisoterapi(IsAuthenticated, GeneratePDF, ListView):
    model = MonitoringFisoterapi
    template_name = 'fisio_terapi/export/monitor.html'
    context_object_name = 'list_fisioterapi'

    def get_pasien_fisioterapi(self):
        return get_object_or_404(PasienFisioterapi, pk=self.kwargs['pasien_id'])
        
    
    def get_queryset(self):
        return super().get_queryset().filter(pasien_fisioterapi=self.get_pasien_fisioterapi())
    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'list_fisioterapi': self.get_queryset(),
                'pasien':self.get_pasien_fisioterapi().pasien,
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Monitoring Fisioterapi {self.get_pasien_fisioterapi().pasien.full_name}'
        )

