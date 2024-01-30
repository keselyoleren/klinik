
from config.form import AbstractForm
from master_data.models import Layanan, PoliKlinik, TenagaMedis
from django import forms


class TenagaMedisForm(AbstractForm):
    class Meta:
        model = TenagaMedis
        fields = '__all__'

    