
from config.choice import StatusRawatPasien
from config.form import AbstractForm, Select2Widget
from pasien.models import Pasien, RawatJalan
from django import forms
from master_data.models import TenagaMedis


class RawatJalanForm(AbstractForm):
    status = forms.ChoiceField(choices=StatusRawatPasien.choices, widget=Select2Widget())
    dokter = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())

    class Meta:
        model = RawatJalan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RawatJalanForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        choices_dokter = [(d.id, d.nama) for d in dokter_queryset]
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['dokter'].choices = choices_dokter
        self.fields['pasien'].choices = choices_pasien



class RegisterPasienRawatJalanForm(AbstractForm):
    class Meta:
        model = RawatJalan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RegisterPasienRawatJalanForm, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()


