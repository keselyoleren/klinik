
from config.form import AbstractForm
from pasien.models import PermintaanLabor, PermintaanLabor2
from django import forms

class PermintaanLaborForm(AbstractForm):
    class Meta:
        model = PermintaanLabor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PermintaanLaborForm, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()
        

class PermintaanLabor2Form(AbstractForm):
    class Meta:
        model = PermintaanLabor2
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PermintaanLabor2Form, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()
        