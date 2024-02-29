# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.contrib import messages

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser, StatusPasien
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.assesment_rawat_jalan_form import AssesmentRawatJalanForm, CpotForm, GcsForm, VasForm, WongBakerForm
from pasien.models import AssesmentRawatJalan, Cpot, Gcs, Pasien, RawatJalan, Vas, WongBaker


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
        wongbraker_formset = inlineformset_factory(AssesmentRawatJalan, WongBaker, form=WongBakerForm, extra=1, can_delete=True)
        vas_formset = inlineformset_factory(AssesmentRawatJalan, Vas, form=VasForm, extra=1, can_delete=True)
        cpot_formset = inlineformset_factory(AssesmentRawatJalan, Cpot, form=CpotForm, extra=1, can_delete=True)
        gcs_formset = inlineformset_factory(AssesmentRawatJalan, Gcs, form=GcsForm, extra=1, can_delete=True)
        if self.request.POST:
            context['wongbraker_formset'] = wongbraker_formset(self.request.POST, self.request.FILES, instance=self.object)
            context['vas_formset'] = vas_formset(self.request.POST, self.request.FILES, instance=self.object)
            context['cpot_formset'] = cpot_formset(self.request.POST, self.request.FILES, instance=self.object)
            context['gcs_formset'] = gcs_formset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['wongbraker_formset'] = wongbraker_formset()
            context['vas_formset'] = vas_formset()
            context['cpot_formset'] = cpot_formset()
            context['gcs_formset'] = gcs_formset()
        return context

  
    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = RawatJalan.objects.get(pk=self.kwargs['pasien_id'])
        response =  super().form_valid(form)
        wongbraker_formset = inlineformset_factory(AssesmentRawatJalan, WongBaker, form=WongBakerForm, extra=1, can_delete=True)
        vas_formset = inlineformset_factory(AssesmentRawatJalan, Vas, form=VasForm, extra=1, can_delete=True)
        cpot_formset = inlineformset_factory(AssesmentRawatJalan, Cpot, form=CpotForm, extra=1, can_delete=True)
        gcs_formset = inlineformset_factory(AssesmentRawatJalan, Gcs, form=GcsForm, extra=1, can_delete=True)
        wong_braker = wongbraker_formset(self.request.POST, instance=self.object)
        vas = vas_formset(self.request.POST, instance=self.object)
        cpot = cpot_formset(self.request.POST, instance=self.object)
        gcs = gcs_formset(self.request.POST, instance=self.object)
        
        if gcs.is_valid():
            gcs.save()
        if wong_braker.is_valid():
            wong_braker.save()
        if vas.is_valid():
            vas.save()
        if cpot.is_valid():
            cpot.save()

        messages.success(self.request, 'Update success')
        return response
        

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
        wongbraker_formset = inlineformset_factory(AssesmentRawatJalan, WongBaker, form=WongBakerForm, extra=1, can_delete=True)
        vas_formset = inlineformset_factory(AssesmentRawatJalan, Vas, form=VasForm, extra=1, can_delete=True)
        cpot_formset = inlineformset_factory(AssesmentRawatJalan, Cpot, form=CpotForm, extra=1, can_delete=True)
        gcs_formset = inlineformset_factory(AssesmentRawatJalan, Gcs, form=GcsForm, extra=1, can_delete=True)
        context['wongbraker_formset'] = wongbraker_formset(instance=self.get_object())
        context['vas_formset'] = vas_formset(instance=self.get_object())
        context['cpot_formset'] = cpot_formset(instance=self.get_object())
        context['gcs_formset'] = gcs_formset(instance=self.get_object())
        return context


    def form_valid(self, form):
        form.instance.pasien_rawat_jalan = self.get_object().pasien_rawat_jalan
        response =  super().form_valid(form)
        wongbraker_formset = inlineformset_factory(AssesmentRawatJalan, WongBaker, form=WongBakerForm, extra=1, can_delete=True)
        vas_formset = inlineformset_factory(AssesmentRawatJalan, Vas, form=VasForm, extra=1, can_delete=True)
        cpot_formset = inlineformset_factory(AssesmentRawatJalan, Cpot, form=CpotForm, extra=1, can_delete=True)
        wongbraker_formset = wongbraker_formset(self.request.POST, instance=self.get_object())
        vas_formset = vas_formset(self.request.POST, instance=self.get_object())
        cpot_formset = cpot_formset(self.request.POST, instance=self.get_object())
        if wongbraker_formset.is_valid():
            wongbraker_formset.save()
        if vas_formset.is_valid():
            vas_formset.save()
        if cpot_formset.is_valid():
            cpot_formset.save()
        messages.success(self.request, 'Update success')
        return response
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

