# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.models import AssesMentFisioTerapi, InformedConsent, PasienFisioterapi, Pasien, PasienFisioterapi, ResumeFisioterapi, RujukanKeluar
from pasien.form.fisioterapi_form import PasienFisioterapiForm

class PasienFisioterapiListView(IsAuthenticated, ListView):
    model = PasienFisioterapi
    template_name = 'fisio_terapi/list.html'
    context_object_name = 'list_fisio_terapi'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Fisioterapi'
        context['header_title'] = 'List Pasien Fisioterapi'
        context['btn_add'] = True
        
        context['create_url'] = reverse_lazy('fisio_terapi-create')
        return context

class PasienFisioterapiCreateView(IsAuthenticated, CreateView):
    model = PasienFisioterapi
    template_name = 'component/form.html'
    form_class = PasienFisioterapiForm
    success_url = reverse_lazy('fisio_terapi-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Fisioterapi'
        context['header_title'] = 'Tambah Pasien Fisioterapi'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class PasienFisioterapiUpdateView(IsAuthenticated, UpdateView):
    model = PasienFisioterapi
    template_name = 'fisio_terapi/detail.html'
    form_class = PasienFisioterapiForm
    success_url = reverse_lazy('fisio_terapi-list')
    context_object_name = 'fisioterapi'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Fisioterapi'
        context['pasien'] = Pasien.objects.get(pk=self.get_object().pasien.id)

        if assesment_fisioterapi := AssesMentFisioTerapi.objects.filter(pasien_fisioterapi=self.get_object()).first():
            context['btn_assesment_fisioterapi_update'] = True
            context['btn_assesment_fisioterapi_update_url'] = reverse_lazy('assesment-fisioterapi-update', kwargs={'pk': assesment_fisioterapi.id})
        

        if rujukan_keluar := RujukanKeluar.objects.filter(pasien_fisioterapi=self.get_object()).first():
            context['btn_rujukan_keluar_update'] = True
            context['btn_rukukan_keluar_update_url'] = reverse_lazy('rujukan_keluar-update', kwargs={'pk': rujukan_keluar.id})

        if resume_fisioterapi := ResumeFisioterapi.objects.filter(pasien_fisioterapi=self.get_object()).first():
            context['btn_resume_fisioterapi_update'] = True
            context['btn_resume_fisioterapi_update_url'] = reverse_lazy('resume_fisioterapi-update', kwargs={'pk': resume_fisioterapi.id})

        if informed_concent := InformedConsent.objects.filter(pasien_fisioterapi=self.get_object()).first():
            context['btn_informed_concent_update'] = True
            context['btn_informed_concent_update_url'] = reverse_lazy('informed-update', kwargs={'pk': informed_concent.id})
        
        context['header_title'] = 'Edit Pasien Fisioterapi'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class PasienFisioterapiDeleteView(IsAuthenticated, DeleteView):
    model = PasienFisioterapi
    template_name = 'component/delete.html'
    success_url = reverse_lazy('fisio_terapi-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Pasien Fisioterapi'
        context['header_title'] = 'Delete Pasien Fisioterapi'
        return context
