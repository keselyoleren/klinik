# myapp/views.py

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404


from django.contrib import messages
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.assesment_fisioterapi_form import InterfensiForm
from pasien.form.fisioterapi_form import ResumeFisioterapiForm

from pasien.models import ResumeFisioterapi, Intervensi, Pasien, PasienFisioterapi


class ResumeFisioterapiCreateView(IsAuthenticated, CreateView):
    model = ResumeFisioterapi
    template_name = 'fisio_terapi/form_resume.html'
    form_class = ResumeFisioterapiForm
    
    def get_pasien_fisioterapi(self):
        return get_object_or_404(PasienFisioterapi, pk=self.kwargs['pasien_id'])

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_pasien_fisioterapi().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Resume Fisioterapi'
        context['header_title'] = 'Resume Fisioterapi'
        context['pasien'] = PasienFisioterapi.objects.get(pk=self.kwargs['pasien_id']).pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_pasien_fisioterapi()
        response =  super().form_valid(form)
        messages.success(self.request, 'Data Berhasil Disimpan')
        return response

class ResumeFisioterapiUpdateView(IsAuthenticated, UpdateView):
    model = ResumeFisioterapi
    template_name = 'fisio_terapi/form_resume.html'
    form_class = ResumeFisioterapiForm
    context_object_name = 'resume'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Resume Fisioterapi'
        context['header_title'] = 'Edit Resume Fisioterapi'
        context['pasien'] = self.get_object().pasien_fisioterapi.pasien
        context['btn_delete'] = True
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_object().pasien_fisioterapi
        messages.success(self.request, 'Update success')
        return super().form_valid(form)

class ResumeFisioterapiDeleteView(IsAuthenticated, DeleteView):
    model = ResumeFisioterapi
    template_name = 'component/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Resume Fisioterapi'
        context['header_title'] = 'Delete Resume Fisioterapi'
        return context


class DownloadAssesmentVisioterapiView(IsAuthenticated, GeneratePDF,  UpdateView):
    model = ResumeFisioterapi
    template_name = 'fisio_terapi/export/assesment.html'
    context_object_name = 'assesment'
    form_class = ResumeFisioterapiForm

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

