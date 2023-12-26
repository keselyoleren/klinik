
from config.form import AbstractForm
from master_data.models import Layanan, PoliKlinik, TenagaMedis
from django import forms
from django.contrib.admin.widgets import (
    FilteredSelectMultiple,
    AutocompleteSelect,
)

class TenagaMedisForm(AbstractForm):
    poliklinik = forms.ModelMultipleChoiceField(
        queryset=PoliKlinik.objects.all(), 
        widget=FilteredSelectMultiple("Poli Klinik", is_stacked=False),
        required=False
    )
    class Meta:
        model = TenagaMedis
        fields = '__all__'

    class Media:
        css = {
            'all': ('/static/jazzmin/css/main.css',),
        }
        js = ('/jsi18n',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')