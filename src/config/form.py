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

            if field == 'created_by' and not get_user().is_superuser:
                self.fields['created_by'].widget = forms.HiddenInput()
            
            if field == 'harga_bersih':
                self.fields['harga_bersih'].widget = forms.HiddenInput()

            