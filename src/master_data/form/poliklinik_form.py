
from config.form import AbstractForm
from master_data.models import Layanan, PoliKlinik
from django import forms
from django.contrib.admin.widgets import (
    FilteredSelectMultiple,
    AutocompleteSelect,
)

class PoliKlinikForm(AbstractForm):
    layanan = forms.ModelMultipleChoiceField(
        queryset=Layanan.objects.all(), 
        widget=FilteredSelectMultiple("Layanan", is_stacked=False),
        required=False
    )
    class Meta:
        model = PoliKlinik
        fields = '__all__'

    class Media:
        css = {
            'all': ('/static/jazzmin/css/main.css',),
        }
        js = ('/jsi18n',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')