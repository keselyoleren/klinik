
from config.choice import StatusRawatJalan
from config.form import AbstractForm, Select2Widget
from pasien.models import Pasien, RawatJalan, RekamMedis
from django import forms
from master_data.models import TenagaMedis


class RekamMedisForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = RekamMedis
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RekamMedisForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        choices_dokter = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = choices_dokter
        self.fields['pasien'].widget = forms.HiddenInput()
