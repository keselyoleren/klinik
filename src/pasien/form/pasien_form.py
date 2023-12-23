
from config.form import AbstractForm
from pasien.models import Pasien

class PasienForm(AbstractForm):
    class Meta:
        model = Pasien
        fields = '__all__'

