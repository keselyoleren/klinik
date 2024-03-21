# myapp/views.py

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404


from django.contrib import messages
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.assesment_fisioterapi_form import AssesmentFisioterapiForm, InterfensiForm

from pasien.models import AssesMentFisioTerapi, Intervensi, Pasien, PasienFisioterapi


class AssesMentFisioTerapiCreateView(IsAuthenticated, CreateView):
    model = AssesMentFisioTerapi
    template_name = 'fisio_terapi/form_assesment.html'
    form_class = AssesmentFisioterapiForm
    
    def get_pasien_fisioterapi(self):
        return get_object_or_404(PasienFisioterapi, pk=self.kwargs['pasien_id'])

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_pasien_fisioterapi().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Awal Pasien Fisioterapi'
        context['header_title'] = 'Assesmen Awal Pasien Fisioterapi'
        context['pasien'] = PasienFisioterapi.objects.get(pk=self.kwargs['pasien_id']).pasien
        RelatedModelFormSet = inlineformset_factory(AssesMentFisioTerapi, Intervensi, form=InterfensiForm, extra=1, can_delete=True)
        if self.request.POST:
            context['related_model_formset'] = RelatedModelFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['related_model_formset'] = RelatedModelFormSet(instance=self.object)
        return context


    # def form_valid(self, form):
    #     form.instance.pasien_fisioterapi = self.get_pasien_fisioterapi()
    #     form.save()
    #     response = super().form_valid(form)

    #     # Process the inline formset
    #     RelatedModelFormSet = inlineformset_factory(AssesMentFisioTerapi, Intervensi, form=InterfensiForm, extra=1, can_delete=True)
    #     formset = RelatedModelFormSet(self.request.POST)
    #     print(formset)

    #     if formset.is_valid():
    #         formset.save()
    #     messages.success(self.request, 'Data Berhasil Disimpan')
    #     return response

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_pasien_fisioterapi()
        response =  super().form_valid(form)
        RelatedModelFormSet = inlineformset_factory(AssesMentFisioTerapi, Intervensi, form=InterfensiForm, extra=1, can_delete=True)
        formset = RelatedModelFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
        messages.success(self.request, 'Data Berhasil Disimpan')
        return response

class AssesMentFisioTerapiUpdateView(IsAuthenticated, UpdateView):
    model = AssesMentFisioTerapi
    template_name = 'fisio_terapi/form_assesment.html'
    form_class = AssesmentFisioterapiForm
    context_object_name = 'assesment'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Awal Pasien Fisioterapi'
        context['header_title'] = 'Edit Assesmen Awal Pasien Fisioterapi'
        context['pasien'] = self.get_object().pasien_fisioterapi.pasien
        RelatedModelFormSet = inlineformset_factory(AssesMentFisioTerapi, Intervensi, form=InterfensiForm, extra=1, can_delete=True)
        context['related_model_formset'] = RelatedModelFormSet(instance=self.get_object())
        context['btn_delete'] = True
        return context

    def form_valid(self, form):
        form.instance.pasien_fisioterapi = self.get_object().pasien_fisioterapi
        RelatedModelFormSet = inlineformset_factory(AssesMentFisioTerapi, Intervensi, form=InterfensiForm, extra=1, can_delete=True)
        formset = RelatedModelFormSet(self.request.POST, instance=self.get_object())
        if formset.is_valid():
            formset.save()
        messages.success(self.request, 'Update success')
        return super().form_valid(form)

class AssesMentFisioTerapiDeleteView(IsAuthenticated, DeleteView):
    model = AssesMentFisioTerapi
    template_name = 'component/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('fisio_terapi-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Awal Pasien Fisioterapi'
        context['header_title'] = 'Delete Assesmen Awal Pasien Fisioterapi'
        return context


class DownloadAssesmentAwalVisioterapiView(IsAuthenticated, GeneratePDF,  UpdateView):
    model = AssesMentFisioTerapi
    template_name = 'fisio_terapi/export/assesment.html'
    context_object_name = 'assesment'
    form_class = AssesmentFisioterapiForm

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

