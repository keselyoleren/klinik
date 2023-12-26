
from config.form import AbstractForm
from pasien.models import RawatJalan

class RawatJalanForm(AbstractForm):
    class Meta:
        model = RawatJalan
        fields = '__all__'

