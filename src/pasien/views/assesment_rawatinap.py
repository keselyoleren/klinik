# myapp/views.py

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404


from django.contrib import messages
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.assesment_rawatinap import AssesmentRawatInapForm, PemerikasanPenunjangForm, RiwayatOperasiForm

from pasien.models import AssessmentRawatInap, PemerikasanPenunjang, RawatInap, RiwayatOperasi


class AssessmentRawatInapCreateView(IsAuthenticated, CreateView):
    model = AssessmentRawatInap
    template_name = 'rawat_inap/form_assesment.html'
    form_class = AssesmentRawatInapForm
    
    def get_pasien_fisioterapi(self):
        return get_object_or_404(RawatInap, pk=self.kwargs['pasien_id'])

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_inap-update', kwargs={'pk': self.get_pasien_fisioterapi().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Pasien Rawat Inap'
        context['header_title'] = 'Assesmen Pasien Rawat Inap'
        context['pasien'] = RawatInap.objects.get(pk=self.kwargs['pasien_id']).pasien
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        if self.request.POST:
            context['riwayat_operasi_formset'] = riwayat_operasi_formset(self.request.POST, self.request.FILES, instance=self.object)
            context['pemeriksaan_penunjang_formset'] = pemeriksaan_penunjang_formset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['riwayat_operasi_formset'] = riwayat_operasi_formset()
            context['pemeriksaan_penunjang_formset'] = pemeriksaan_penunjang_formset()
        return context
    
    def form_valid(self, form):
        form.instance.pasien_rawat_inap = RawatInap.objects.get(pk=self.kwargs['pasien_id'])
        response = super().form_valid(form)
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        operasi = riwayat_operasi_formset(self.request.POST, instance=self.object)
        pemeriksaan_penunjang = pemeriksaan_penunjang_formset(self.request.POST, instance=self.object)
        if operasi.is_valid():
            operasi.save()
        if pemeriksaan_penunjang.is_valid():
            pemeriksaan_penunjang.save()
        messages.success(self.request, 'Create success')
        return response

class AssessmentRawatInapUpdateView(IsAuthenticated, UpdateView):
    model = AssessmentRawatInap
    template_name = 'rawat_inap/form_assesment.html'
    form_class = AssesmentRawatInapForm
    context_object_name = 'assesment'

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_inap-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Pasien Rawat Inap'
        context['header_title'] = 'Edit Assesmen Pasien Rawat Inap'
        context['pasien'] = self.get_object().pasien_fisioterapi.pasien
        context['btn_delete'] = True
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        context['pemeriksaan_penunjang_formset'] = pemeriksaan_penunjang_formset(instance=self.get_object())
        context['riwayat_operasi_formset'] = riwayat_operasi_formset(instance=self.get_object())
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_inap = self.get_object().pasien_rawat_inap
        response = super().form_valid(form)
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        pemeriksaan_penunjang = pemeriksaan_penunjang_formset(self.request.POST, instance=self.get_object())
        operasi = riwayat_operasi_formset(self.request.POST, instance=self.get_object())
        if operasi.is_valid():
            operasi.save()
        if pemeriksaan_penunjang.is_valid():
            pemeriksaan_penunjang.save()

        messages.success(self.request, 'Create success')
        return response

class AssessmentRawatInapDeleteView(IsAuthenticated, DeleteView):
    model = AssessmentRawatInap
    template_name = 'component/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_inap-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Pasien Rawat Inap'
        context['header_title'] = 'Delete Assesmen Pasien Rawat Inap'
        return context


class DownloadAssesmentVisioterapiView(IsAuthenticated, GeneratePDF,  UpdateView):
    model = AssessmentRawatInap
    template_name = 'rawat_inap/export/assesment.html'
    context_object_name = 'assesment'
    form_class = AssesmentRawatInapForm

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

