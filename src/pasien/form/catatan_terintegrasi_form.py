
from config.choice import StatusRawatJalan
from config.form import AbstractForm, Select2Widget
from pasien.models import AssesmentRawatJalan, Pasien, RawatJalan, CatatanTerIntegrasi
from django import forms
from master_data.models import TenagaMedis


class CatanTerintegrasiForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    

    class Meta:
        model = CatatanTerIntegrasi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CatanTerintegrasiForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis
        