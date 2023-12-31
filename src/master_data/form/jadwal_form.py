
from config.form import AbstractForm
from django import forms
from config.form import AbstractForm, Select2Widget
from master_data.models import JadwalTenagaMedis, TenagaMedis

class JadwalTenagaMedisForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = JadwalTenagaMedis
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(JadwalTenagaMedisForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        choices_dokter = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = choices_dokter

    