from django.utils.translation import gettext as _
from config.choice import JenisKelamin, StatusPasien, StatusRawatJalan
from config.models import BaseModel
from django.db import models

# Create your models here.
class Pasien(BaseModel):
    full_name = models.CharField(_("Nama Lengkap"), max_length=255)
    phone = models.CharField(_("No.Telepon"), max_length=255, blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True, null=True)
    tempat_lahir = models.CharField(_("Tempat Lahir"), max_length=255, blank=True, null=True)
    tanggal_lahir = models.DateField(_("Tanggal Lahir"), blank=True, null=True)
    jenis_kelamin = models.CharField(_("Jenis Kelamin"), max_length=255, choices=JenisKelamin.choices, blank=True, null=True)
    nik = models.CharField(_("Nomor Kartu Identitas"), max_length=255)
    no_rekam_pedis = models.CharField(_("Nomor Rekam Medis"), max_length=255)
    nama_ibu = models.CharField(_("Nama Ibu Kandung"), max_length=255, blank=True, null=True)
    
    agama = models.CharField(_("Agama"), max_length=255, blank=True, null=True)
    penddikan_terakhir = models.CharField(_("Pendidikan Terakhir"), max_length=255, blank=True, null=True)
    pekerjaan = models.CharField(_("Pekerjaan"), max_length=255, blank=True, null=True)
    alamat_kartu_identitas = models.TextField(_("Alamat Kartu Identitas"), blank=True, null=True)
    alamat_domisili = models.TextField(_("Alamat Domisili"), blank=True, null=True)
    status = models.CharField(_("Status"), max_length=255, choices=StatusPasien.choices, default=StatusPasien.AKTIF)
    

    def __str__(self) -> str:
        return self.full_name


class RawatJalan(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Pasien"), on_delete=models.CASCADE)
    poli_klinik = models.ForeignKey('master_data.PoliKlinik', verbose_name=_("Poli Klinik"), on_delete=models.CASCADE)
    dokter = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Dokter"), on_delete=models.CASCADE)
    waktu_konsultasi = models.DateTimeField(_("Waktu Konsultasi"), blank=True, null=True)
    status = models.CharField(_("Status"), max_length=255, choices=StatusRawatJalan.choices, default=StatusRawatJalan.REGISTRASI)

    def __str__(self) -> str:
        return self.pasien.full_name


class RekamMedis(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Nama Pasien"), on_delete=models.CASCADE)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Tenaga Medis"), on_delete=models.CASCADE)
    keluhan_utama = models.TextField(_("Keluhan Utama"), blank=True, null=True)
    riwayat_penyakit = models.CharField(_("Riwayat Penyakit"), max_length=255, blank=True, null=True)
    riwayat_alergi = models.CharField(_("Riwayat Alergi"), max_length=255, blank=True, null=True)
    tanda_vital = models.JSONField(_("Tanda - tanda  Vital"), blank=True, null=True)