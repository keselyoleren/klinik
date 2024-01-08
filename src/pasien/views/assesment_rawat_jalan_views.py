# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusPasien
from config.permis import IsAuthenticated, IsAuthenticated
from pasien.form.assesment_rawat_jalan_form import AssesmentRawatJalanForm
from pasien.models import AssesmentRawatJalan, Pasien


class AssesmentRawatJalanCreateView(IsAuthenticated, CreateView):
    model = AssesmentRawatJalan
    template_name = 'rawat_jalan/form_assesment.html'
    form_class = AssesmentRawatJalanForm
    success_url = reverse_lazy('rawat_jalan-list')

    def get_context_data(self, **kwargs):
        print(Pasien.objects.get(pk=self.kwargs['pasien_id']))
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Awal Pasien Rawat Jalan'
        context['header_title'] = 'Assesmen Awal Pasien Rawat Jalan'
        context['pasien'] = Pasien.objects.get(pk=self.kwargs['pasien_id'])
        return context

    def form_valid(self, form):
        form.instance.pasien = Pasien.objects.get(id=self.kwargs['pasien_id'])
        form.save()
        return super().form_valid(form)

class AssesmentRawatJalanUpdateView(IsAuthenticated, UpdateView):
    model = AssesmentRawatJalan
    template_name = 'component/form.html'
    form_class = AssesmentRawatJalanForm
    success_url = reverse_lazy('rawat_jalan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Jalan'
        context['header_title'] = 'Edit Rawat Jalan'
        return context

    def form_valid(self, form):
        form.instance.pasien = self.get_object().pasien
        return super().form_valid(form)

class AssesmentRawatJalanDeleteView(IsAuthenticated, DeleteView):
    model = AssesmentRawatJalan
    template_name = 'component/delete.html'
    success_url = reverse_lazy('rawat_jalan-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Rawat Jalan'
        context['header_title'] = 'Delete Rawat Jalan'
        return context
