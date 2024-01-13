
from config.form import AbstractForm
from pasien.models import Obat

class ObatForm(AbstractForm):
    class Meta:
        model = Obat
        fields = '__all__'

