from django.contrib import admin
from pasien.form.assesment_fisioterapi_form import InterfensiForm
from pasien.models import AssesMentFisioTerapi, Intervensi, Pasien, RekamMedis
from django.utils.translation import gettext as _

# Register your models here.
@admin.register(Pasien)
class PasienAdminView(admin.ModelAdmin):
    list_display = ('full_name', 'jenis_kelamin', 'status')

@admin.register(RekamMedis)
class RekamMedisAdminView(admin.ModelAdmin):
     fieldsets = (
        (None, {'fields': ('pasien', 'tenaga_medis', 'keluhan_utama', 'status_perokok', 'riwayat_penyakit', 'riwayat_alergi')}),
        (_('Tanda - Tanda Vital'), {
            'fields': ('suhu_tubuh', 'nadi', 'sistole', 'diastole', 'frekuensi_pernafasan'),
        }),
        (_('Pemeriksaan Fisik'), {'fields': ('tinggi_badan', 'berat_badan', 'imt')}),
    )


class IntervensiInline(admin.TabularInline):
    model = Intervensi
    form = InterfensiForm


@admin.register(AssesMentFisioTerapi)
class AssesmentFisioTerapiAdminView(admin.ModelAdmin):
    inlines = (IntervensiInline,)