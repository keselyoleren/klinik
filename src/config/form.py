from webbrowser import get
from django import forms
from config.choice import RoleUser
from django import forms
from django.forms.widgets import Select
from django.contrib.admin.widgets import (
    FilteredSelectMultiple,
    AdminDateWidget,
    AdminSplitDateTime,
)
from config.request import get_user

class Select2Widget(Select):
    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        if attrs is None:
            attrs = {}
        attrs['class'] = attrs.get('class', '') + ' select2 form-control'
        super().__init__(attrs=attrs, choices=choices, *args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.update({'class': ' '.join(attrs.get('class', '').split() + ['select2', 'form-control'])})
        return attrs

class AbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            if field == 'tanggal_lahir':
                self.fields['tanggal_lahir'].widget = forms.DateInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })

            if field == 'tanggal_kematian':
                self.fields['tanggal_kematian'].widget = forms.DateInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })

            if field == 'waktu_konsultasi':
                self.fields['waktu_konsultasi'].widget = forms.DateTimeInput(attrs={
                    'type':'datetime-local',
                    'class': 'form-control',
                })

            if field == 'jam_mulai':
                self.fields['jam_mulai'].widget = forms.TimeInput(attrs={
                    'type':'time',
                    'class': 'form-control',
                })

            if field == 'jam_selesai':
                self.fields['jam_selesai'].widget = forms.TimeInput(attrs={
                    'type':'time',
                    'class': 'form-control',
                })

            if field == 'obat':
                self.fields['obat'].widget = forms.HiddenInput()

            if field == 'created_by' and not get_user().is_superuser:
                self.fields['created_by'].widget = forms.HiddenInput()
            
            if field == 'harga_bersih':
                self.fields['harga_bersih'].widget = forms.HiddenInput()

            if field == 'pasien_rawat_jalan':
                self.fields['pasien_rawat_jalan'].widget = forms.HiddenInput()

            if field == 'pasien_fisioterapi':
                self.fields['pasien_fisioterapi'].widget = forms.HiddenInput()
            
            if field == 'pasien_rawat_inap':
                self.fields['pasien_rawat_inap'].widget = forms.HiddenInput()

            if field == 'tanggal':
                self.fields['tanggal'].widget = forms.DateInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })

            if field == 'start':
                self.fields['start'].widget = forms.DateInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })

            if field == 'end':
                self.fields['end'].widget = forms.DateInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })

            if field == 'tgl_masuk':
                self.fields['tgl_masuk'].widget = forms.DateInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })
            
            if field == 'tgl_keluar':
                self.fields['tgl_keluar'].widget = forms.DateInput(attrs={
                    'type':'date',
                    'class': 'form-control',
                })

            if field == 'jam':
                self.fields['jam'].widget = forms.TimeInput(attrs={
                    'type':'time',
                    'class': 'form-control',
                })