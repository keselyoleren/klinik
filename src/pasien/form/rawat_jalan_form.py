
from config.choice import StatusRawatJalan
from config.form import AbstractForm, Select2Widget
from pasien.models import RawatJalan
from django import forms
from master_data.models import TenagaMedis


class RawatJalanForm(AbstractForm):
    status = forms.ChoiceField(choices=StatusRawatJalan.choices, widget=Select2Widget())
    # dokter = forms.ChoiceField(widget=Select2Widget())

    class Meta:
        model = RawatJalan
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(RawatJalanForm, self).__init__(*args, **kwargs)
    #     dokter_queryset = TenagaMedis.objects.all()
    #     choices = [(d.id, d.nama) for d in dokter_queryset]
    #     self.fields['dokter'].choices = choices