
from config.choice import StatusAlergi, StatusRawatPasien
from config.form import AbstractForm, Select2Widget
from pasien.models import AssesmentRawatJalan, Cpot, Gcs, Pasien, RawatJalan, Vas, WongBaker
from django import forms
from master_data.models import TenagaMedis


class AssesmentRawatJalanForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    

    class Meta:
        model = AssesmentRawatJalan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AssesmentRawatJalanForm, self).__init__(*args, **kwargs)
        dokter_queryset = TenagaMedis.objects.all()
        tenaga_medis = [(d.id, d.nama) for d in dokter_queryset]
        self.fields['tenaga_medis'].choices = tenaga_medis
        
class WongBakerForm(AbstractForm):
    class Meta:
        model = WongBaker
        fields = "__all__"

class VasForm(AbstractForm):
    class Meta:
        model = Vas
        fields = "__all__"

class CpotForm(AbstractForm):
    class Meta:
        model = Cpot
        fields = "__all__"
        
class GcsForm(AbstractForm):
    class Meta:
        model = Gcs
        fields = "__all__"
        

