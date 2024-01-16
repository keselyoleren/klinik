
from config.form import AbstractForm
from config.form import AbstractForm
from master_data.models import InventoryObat, ObatMasuk, ObatKeluar

class InfentoryObatForm(AbstractForm):
    class Meta:
        model = InventoryObat
        fields = "__all__"

class ObatMasukForm(AbstractForm):
    class Meta:
        model = ObatMasuk
        fields = '__all__'

class ObatKeluarForm(AbstractForm):
    class Meta:
        model = ObatKeluar
        fields = '__all__'


        
