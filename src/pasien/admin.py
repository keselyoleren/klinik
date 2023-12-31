from django.contrib import admin
from pasien.models import Pasien, RekamMedis

# Register your models here.
@admin.register(Pasien)
class PasienAdminView(admin.ModelAdmin):
    list_display = ('full_name', 'jenis_kelamin', 'status', 'no_rekam_pedis')

@admin.register(RekamMedis)
class RekamMedisAdminView(admin.ModelAdmin):
    pass