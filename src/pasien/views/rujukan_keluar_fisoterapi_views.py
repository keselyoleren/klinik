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
from pasien.form.fisioterapi_form import RujukanKeluarForm

from pasien.models import RujukanKeluar, Intervensi, Pasien, PasienFisioterapi


class RujukanKeluarCreateView(IsAuthenticated, CreateView):
    model = RujukanKeluar
    template_name = 'fisio_terapi/form_surat_keluar.html'
    form_class = RujukanKeluarForm
    
    def get_pasien_fisioterapi(self):
        return get_object_or_404(PasienFisioterapi, pk=self.kwargs['pasien_id'])

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_pasien_fisioterapi().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rujukan Keluar Fisioterapi'
        context['header_title'] = 'Rujukan Keluar Fisioterapi'
        context['pasien'] = PasienFisioterapi.objects.get(pk=self.kwargs['pasien_id']).pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_pasien_fisioterapi()
        response =  super().form_valid(form)
        messages.success(self.request, 'Data Berhasil Disimpan')
        return response

class RujukanKeluarUpdateView(IsAuthenticated, UpdateView):
    model = RujukanKeluar
    template_name = 'fisio_terapi/form_surat_keluar.html'
    form_class = RujukanKeluarForm
    context_object_name = 'rujukan_keluar'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rujukan Keluar Fisioterapi'
        context['header_title'] = 'Edit Rujukan Keluar Fisioterapi'
        context['pasien'] = self.get_object().pasien_fisioterapi.pasien
        context['btn_delete'] = True
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_object().pasien_fisioterapi
        messages.success(self.request, 'Update success')
        return super().form_valid(form)

class RujukanKeluarDeleteView(IsAuthenticated, DeleteView):
    model = RujukanKeluar
    template_name = 'component/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rujukan Keluar Fisioterapi'
        context['header_title'] = 'Delete Rujukan Keluar Fisioterapi'
        return context


class DownloadAssesmentVisioterapiView(IsAuthenticated, GeneratePDF,  UpdateView):
    model = RujukanKeluar
    template_name = 'fisio_terapi/export/assesment.html'
    context_object_name = 'assesment'
    form_class = RujukanKeluarForm

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

