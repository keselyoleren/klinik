
from re import I
from config.form import AbstractForm, Select2Widget
from pasien.models import AssessmentRawatInap, PemerikasanPenunjang, RiwayatOperasi
from django import forms
from master_data.models import TenagaMedis


class AssesmentRawatInapForm(AbstractForm):    
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    

    class Meta:
        model = AssessmentRawatInap
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AssesmentRawatInapForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis
        self.fields['autoanamnesis'].widget.attrs['class'] = ''
        self.fields['alloanamnesis'].widget.attrs['class'] = ''
        self.fields['dengan'].widget.attrs['class'] = ''
        self.fields['hubungan_dengan'].widget.attrs['class'] = ''
        self.fields['pasien_rawat_inap'].widget = forms.HiddenInput()

class RiwayatOperasiForm(AbstractForm):
    class Meta:
        model = RiwayatOperasi
        fields = "__all__"

class PemerikasanPenunjangForm(AbstractForm):
    class Meta:
        model = PemerikasanPenunjang
        fields = "__all__"