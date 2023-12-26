from django.contrib import admin

from master_data.models import Layanan, PoliKlinik

# Register your models here.
@admin.register(Layanan)
class LayananAdminView(admin.ModelAdmin):
    list_display = ['nama_layanan', 'kode_layanan', 'harga_bersih']


@admin.register(PoliKlinik)
class PoliKlinikAdminView(admin.ModelAdmin):
    list_display = ['nama_poli', 'keterangan']