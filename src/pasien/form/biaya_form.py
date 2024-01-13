
from config.form import AbstractForm
from pasien.models import Pasien, RincianBiaya

class RincianBiayaForm(AbstractForm):
    class Meta:
        model = RincianBiaya
        fields = '__all__'

