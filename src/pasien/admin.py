from django.contrib import admin
from pasien.models import Pasien, RekamMedis
from django.utils.translation import gettext as _

# Register your models here.
@admin.register(Pasien)
class PasienAdminView(admin.ModelAdmin):
    list_display = ('full_name', 'jenis_kelamin', 'status', 'no_rekam_pedis')

@admin.register(RekamMedis)
class RekamMedisAdminView(admin.ModelAdmin):
     fieldsets = (
        (None, {'fields': ('pasien', 'tenaga_medis', 'keluhan_utama', 'status_perokok', 'riwayat_penyakit', 'riwayat_alergi')}),
        (_('Tanda - Tanda Vital'), {
            'fields': ('suhu_tubuh', 'nadi', 'sistole', 'diastole', 'frekuensi_pernafasan'),
        }),
        (_('Pemeriksaan Fisik'), {'fields': ('tinggi_badan', 'berat_badan', 'imt')}),
    )