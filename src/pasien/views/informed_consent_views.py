# myapp/views.py

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


from django.contrib import messages
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.fisioterapi_form import InformedConsentForm

from pasien.models import InformedConsent, PasienFisioterapi


class InformedConsentCreateView(IsAuthenticated, CreateView):
    model = InformedConsent
    template_name = 'fisio_terapi/form_informed.html'
    form_class = InformedConsentForm
    
    def get_pasien_fisioterapi(self):
        return get_object_or_404(PasienFisioterapi, pk=self.kwargs['pasien_id'])

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_pasien_fisioterapi().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Informed Consent Fisioterapi'
        context['header_title'] = 'Informed Consent Fisioterapi'
        context['pasien'] = PasienFisioterapi.objects.get(pk=self.kwargs['pasien_id']).pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_pasien_fisioterapi()
        response =  super().form_valid(form)
        messages.success(self.request, 'Data Berhasil Disimpan')
        return response

class InformedConsentUpdateView(IsAuthenticated, UpdateView):
    model = InformedConsent
    template_name = 'fisio_terapi/form_informed.html'
    form_class = InformedConsentForm
    context_object_name = 'informed'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Informed Consent Fisioterapi'
        context['header_title'] = 'Edit Informed Consent Fisioterapi'
        context['pasien'] = self.get_object().pasien_fisioterapi.pasien
        context['btn_delete'] = True
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_object().pasien_fisioterapi
        messages.success(self.request, 'Update success')
        return super().form_valid(form)

class InformedConsentDeleteView(IsAuthenticated, DeleteView):
    model = InformedConsent
    template_name = 'component/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Informed Consent Fisioterapi'
        context['header_title'] = 'Delete Informed Consent Fisioterapi'
        return context


class DownloadInvormedApiView(IsAuthenticated, GeneratePDF,  UpdateView):
    model = InformedConsent
    template_name = 'fisio_terapi/export/informed.html'
    context_object_name = 'informed'
    form_class = InformedConsentForm

    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'assesment': self.get_object(),
                'pasien':self.get_object().pasien_fisioterapi,
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Assesment Pasien Fisioterapi {self.get_object().pasien_fisioterapi.pasien.full_name}'
        )

