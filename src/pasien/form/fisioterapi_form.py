
from config.form import AbstractForm, Select2Widget
from pasien.models import Pasien, PasienFisioterapi
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


