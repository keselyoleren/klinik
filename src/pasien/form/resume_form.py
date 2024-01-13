
from django import forms
from config.form import AbstractForm, Select2Widget
from pasien.models import Obat,  Resume
from master_data.models import TenagaMedis

class ResumeForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    

    class Meta:
        model = Resume
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis
        