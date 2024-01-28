
from config.form import AbstractForm, Select2Widget
from pasien.models import InformedConsent, MonitoringFisoterapi, Pasien, PasienFisioterapi, ResumeFisioterapi, RujukanKeluar
from django import forms
from master_data.models import TenagaMedis


class PasienFisioterapiForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())

    class Meta:
        model = PasienFisioterapi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PasienFisioterapiForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['pasien'].choices = choices_pasien


class RegisterPasienFisioterapiForm(AbstractForm):
    class Meta:
        model = PasienFisioterapi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RegisterPasienFisioterapiForm, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()


class RujukanKeluarForm(AbstractForm):    
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    
    class Meta:
        model = RujukanKeluar
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RujukanKeluarForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis
        

class ResumeFisioterapiForm(AbstractForm):    
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    
    class Meta:
        model = ResumeFisioterapi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ResumeFisioterapiForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis
        

class MonitoringFisoterapiForm(AbstractForm):    
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    
    class Meta:
        model = MonitoringFisoterapi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MonitoringFisoterapiForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis

class InformedConsentForm(AbstractForm):    
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    
    class Meta:
        model = InformedConsent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InformedConsentForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis