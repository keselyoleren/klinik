from django.contrib import admin

from master_data.models import Layanan, PoliKlinik

# Register your models here.
@admin.register(Layanan)
class LayananAdminView(admin.ModelAdmin):
    pass


@admin.register(PoliKlinik)
class PoliKlinikAdminView(admin.ModelAdmin):
    list_display = ['nama_poli', 'keterangan']