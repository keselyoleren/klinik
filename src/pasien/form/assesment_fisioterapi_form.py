
from re import I
from config.form import AbstractForm, Select2Widget
from pasien.models import AssesMentFisioTerapi, Intervensi
from django import forms
from master_data.models import TenagaMedis


class AssesmentFisioterapiForm(AbstractForm):    
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    

    class Meta:
        model = AssesMentFisioTerapi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AssesmentFisioterapiForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis
        

class InterfensiForm(AbstractForm):
    class Meta:
        model = Intervensi
        fields = ('intervensi', 'tempat_yang_diterapi')