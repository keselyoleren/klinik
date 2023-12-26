
from config.form import AbstractForm
from master_data.models import Layanan

class LayananForm(AbstractForm):
    class Meta:
        model = Layanan
        fields = '__all__'

