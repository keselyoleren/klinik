
from pyexpat import model
from django.utils.translation import gettext as _
from config.choice import JenisKelamin, StatusPasien
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