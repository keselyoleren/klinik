# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from django.contrib import messages
from config.choice import UnitLayanan
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.form.fisioterapi_form import PasienFisioterapiForm, RegisterPasienFisioterapiForm
from pasien.form.rawat_inap import RegisterPasienRawatInapForm
from pasien.form.rawat_jalan_form import RegisterPasienRawatJalanForm
from pasien.models import Pasien, PasienFisioterapi, RawatInap, RawatJalan
from pasien.form.pasien_form import PasienForm


class PasienListView(IsAuthenticated, ListView):
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

class PasienCreateView(IsAuthenticated, CreateView):
    model = Pasien
    template_name = 'pasien/form.html'
    form_class = PasienForm
    success_url = reverse_lazy('pasien-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien'
        context['header_title'] = 'Tambah Pasien'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Create Pasien Berhasil")
        return super().form_valid(form)

class PasienUpdateView(IsAuthenticated, UpdateView):
    model = Pasien
    template_name = 'pasien/detail.html'
    form_class = PasienForm
    success_url = reverse_lazy('pasien-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien'

        if rawat_jalan := RawatJalan.objects.filter(pasien=self.get_object()).first():
            context['update_pasien_rawat_jalan'] = True
            context['btn_update_pasien_rawat_jalan'] = reverse_lazy('rawat_jalan-update', kwargs={'pk': rawat_jalan.id})

        if pasien_rawat_inap := RawatInap.objects.filter(pasien=self.get_object()).first():
            context['update_pasien_rawat_inap'] = True
            context['btn_update_pasien_rawat_inap'] = reverse_lazy('rawat_inap-update', kwargs={'pk': pasien_rawat_inap.id})

        if pasien_fisio_terapi := PasienFisioterapi.objects.filter(pasien=self.get_object()).first():
            context['update_pasien_fisio_terapi'] = True
            context['btn_update_pasien_fisio_terapi'] = reverse_lazy('fisio_terapi-update', kwargs={'pk': pasien_fisio_terapi.id})

        context['pasien'] = self.get_object()
        context['header_title'] = 'Edit Pasien'
        return context

    def form_valid(self, form):
        context = super().form_valid(form)
        messages.success(self.request, "Update Pasien Berhasil")
        return context

class PasienDeleteView(IsAuthenticated, DeleteView):
    model = Pasien
    template_name = 'component/delete.html'
    success_url = reverse_lazy('pasien-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien'
        context['header_title'] = 'Delete Pasien'
        return context



class PasienRawatJalanRegisterViwe(IsAuthenticated, CreateView):
    model = RawatJalan
    template_name = 'component/form.html'
    form_class = RegisterPasienRawatJalanForm
    

    def get_pasien(self):
        return Pasien.objects.filter(id=self.kwargs['pasien_id'])
    
    def get_pasien_rawat_jalan(self):
        return RawatJalan.objects.filter(pasien_id=self.kwargs['pasien_id']).first()

    def get_success_url(self):
        return reverse_lazy('rawat_jalan-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Rawat Jalan'
        context['header_title'] = 'Register Pasien Rawat Jalan'
        return context

    def form_valid(self, form):
        form.instance.pasien_id = self.kwargs['pasien_id']
        form.save()
        self.get_pasien().update(status=UnitLayanan.RAWAT_JALAN)
        messages.success(self.request, "Register Pasien Rawat Jalan Berhasil")
        return super().form_valid(form)


class PasienRawatInapRegisterView(IsAuthenticated, CreateView):
    model = RawatInap
    template_name = 'component/form.html'
    form_class = RegisterPasienRawatInapForm

    def get_pasien(self):
        return Pasien.objects.filter(id=self.kwargs['pasien_id'])
    

    def get_pasien_rawat_inap(self):
        return RawatInap.objects.filter(pasien_id=self.kwargs['pasien_id']).first()

    def get_success_url(self):
        return reverse_lazy('rawat_inap-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Rawat Inap'
        context['header_title'] = 'Register Pasien Rawat Inap'
        return context

    def form_valid(self, form):
        form.instance.pasien_id = self.kwargs['pasien_id']
        form.save()
        self.get_pasien().update(status=UnitLayanan.RAWAT_INAP)
        messages.success(self.request, "Register Pasien Rawat Inap Berhasil")
        return super().form_valid(form)

class PasienFisioTerapiRegisterView(IsAuthenticated, CreateView):
    model = PasienFisioterapi
    template_name = 'component/form.html'
    form_class = RegisterPasienFisioterapiForm
    

    def get_pasien(self):
        return Pasien.objects.filter(id=self.kwargs['pasien_id'])

    def get_pasien_fisio_terapi(self):
        return PasienFisioterapi.objects.filter(pasien_id=self.kwargs['pasien_id']).first()

    def get_success_url(self):
        return reverse_lazy('fisio_terapi-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Fisio Terapi'
        context['header_title'] = 'Register Pasien Fisio Terapi'
        return context

    def form_valid(self, form):
        form.instance.pasien_id = self.kwargs['pasien_id']
        form.save()
        self.get_pasien().update(status=UnitLayanan.FISIOTERAPI)
        messages.success(self.request, "Register Pasien Fisioterapi Berhasil")
        return super().form_valid(form)