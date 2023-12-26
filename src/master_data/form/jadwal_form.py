
from config.form import AbstractForm
from master_data.models import JadwalTenagaMedis

class JadwalTenagaMedisForm(AbstractForm):
    class Meta:
        model = JadwalTenagaMedis
        fields = '__all__'

    