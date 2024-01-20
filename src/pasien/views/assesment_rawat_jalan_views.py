# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusPasien
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.assesment_rawat_jalan_form import AssesmentRawatJalanForm
from pasien.models import AssesmentRawatJalan, Pasien, RawatJalan


class AssesmentRawatJalanCreateView(IsAuthenticated, CreateView):
    model = AssesmentRawatJalan
    template_name = 'rawat_jalan/form_assesment.html'
    form_class = AssesmentRawatJalanForm
    success_url = reverse_lazy('rawat_jalan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Awal Pasien Rawat Jalan'
        context['header_title'] = 'Assesmen Awal Pasien Rawat Jalan'
        context['pasien'] = RawatJalan.objects.get(pk=self.kwargs['pasien_id']).pasien
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = RawatJalan.objects.get(pk=self.kwargs['pasien_id'])
        form.save()
        return super().form_valid(form)

class AssesmentRawatJalanUpdateView(IsAuthenticated, UpdateView):
    model = AssesmentRawatJalan
    template_name = 'rawat_jalan/form_assesment.html'
    form_class = AssesmentRawatJalanForm
    context_object_name = 'assesment'

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_jalan-update', kwargs={'pk': self.get_object().pasien_rawat_jalan.id})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Awal Pasien Rawat Jalan'
        context['header_title'] = 'Edit Assesmen Awal Pasien Rawat Jalan'
        context['pasien'] = self.get_object().pasien_rawat_jalan.pasien
        context['btn_delete'] = True
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = self.get_object().pasien_rawat_jalan
        return super().form_valid(form)

class AssesmentRawatJalanDeleteView(IsAuthenticated, DeleteView):
    model = AssesmentRawatJalan
    template_name = 'component/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_jalan-update', kwargs={'pk': self.get_object().pasien_rawat_jalan.id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Awal Pasien Rawat Jalan'
        context['header_title'] = 'Delete Assesmen Awal Pasien Rawat Jalan'
        return context


class DownloadAssesmentView(IsAuthenticated, GeneratePDF,  UpdateView):
    model = AssesmentRawatJalan
    template_name = 'rawat_jalan/export/assesment.html'
    context_object_name = 'assesment'
    form_class = AssesmentRawatJalanForm

    def get(self, request, *args, **kwargs):
        return self.render_to_pdf(
            {
                'assesment': self.get_object(),
                'pasien':self.get_object().pasien_rawat_jalan,
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Assesment Awal Rawat Jalan {self.get_object().pasien_rawat_jalan.pasien.full_name}'
        )

