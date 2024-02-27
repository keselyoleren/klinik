# myapp/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.labor_form import PermintaanLabor2Form

from pasien.models import  Pasien, PermintaanLabor2

class PermintaanLabor2ListView(IsAuthenticated, ListView):
    model = PermintaanLabor2
    template_name = 'labor/permintaan2/list.html'
    context_object_name = 'permintaan_labor_list'

    def get_pasien(self):
        return Pasien.objects.get(pk=self.kwargs['pasien_id'])
        
    
    def get_queryset(self):
        try:
            return super().get_queryset().filter(pasien=self.get_pasien())
        except Exception:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Permintaan Laboratorium'
        context['btn_add'] = True
        context['pasien'] = self.get_pasien()
        context['create_url'] = reverse_lazy('permintaan-labor2-create', kwargs={'pasien_id': self.kwargs['pasien_id']})
        return context


class PermintaanLabor2CreateView(IsAuthenticated, CreateView):
    model = PermintaanLabor2
    template_name = 'labor/permintaan2/form.html'
    form_class = PermintaanLabor2Form
    success_url = reverse_lazy('permintaan-labor2-list')

    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor2-list', kwargs={'pasien_id': self.kwargs['pasien_id']})

    def get_pasien(self):
        return Pasien.objects.get(pk=self.kwargs['pasien_id'])
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Permintaan Laboratorium'
        context['pasien'] = self.get_pasien()
        return context

    def form_valid(self, form):
        form.instance.pasien = self.get_pasien()
        form.save()
        return super().form_valid(form)

class PermintaanLabor2UpdateView(IsAuthenticated, UpdateView):
    model = PermintaanLabor2
    template_name = 'labor/permintaan2/form.html'
    form_class = PermintaanLabor2Form


    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor2-list', kwargs={'pasien_id': self.get_object().pasien.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Edit Permintaan Laboratorium'
        context['pasien'] = self.get_object().pasien
        return context

    def form_valid(self, form):
        form.instance.pasien = self.get_object().pasien
        form.save()
        return super().form_valid(form)


class PermintaanLabor2DeleteView(IsAuthenticated, DeleteView):
    model = PermintaanLabor2
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor2-list', kwargs={'pasien_id': self.get_object().pasien.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Delete Permintaan Laboratorium'
        return context


class DownloadPermintaanLabor2(IsAuthenticated, GeneratePDF, DetailView):
    model = PermintaanLabor2
    form_class = PermintaanLabor2Form
    template_name = 'labor/permintaan2/download.html'
    context_object_name = 'hasil_labor'


    
    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'title':'FORMULIR PERMINTAAN PEMERIKSAAN LABORATORIUM',
                'pasien':self.get_object().pasien,
                'created_at':self.get_object().created_at,
                'pemeriksa':self.get_object().pemeriksa,
                'form':self.form_class(instance=self.get_object()),
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Permintaan Laboratorium Pasien {self.get_object().pasien.full_name}'
        )

