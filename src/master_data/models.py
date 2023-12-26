from dis import dis
import email
from statistics import mode
from tkinter.tix import Tree
from django.db import models
from config.choice import Hari
from config.models import BaseModel
from django.utils.translation import gettext as _
# Create your models here.

class Layanan(BaseModel):
    nama_layanan = models.CharField(_("Nama Layanan"), max_length=255)
    kode_layanan = models.CharField(_("Kode Layanan"), max_length=255, blank=True, null=True)
    harga_dasar = models.IntegerField(_("Harga Dasar"))
    diskon = models.IntegerField(_("Diskon"), default=0)
    harga_bersih = models.IntegerField(_("Harga Bersih"), null=True, blank=True, default=0)
    keterangan = models.TextField(_("Keterangan"), blank=True, null=True)

    def __str__(self) -> str:
        return self.nama_layanan

    def save(self, *args, **kwargs):
        if self.diskon == 0:
            self.harga_bersih = self.harga_dasar
        else:
            total_diskon = (self.harga_dasar * self.diskon) / 100
            self.harga_bersih = self.harga_dasar - total_diskon
        super(Layanan, self).save(*args, **kwargs)


class PoliKlinik(BaseModel):
    nama_poli = models.CharField(_("Nama Poliklinik"), max_length=255)
    layanan = models.ManyToManyField(Layanan, verbose_name=_("Layanan"))
    keterangan = models.TextField(_("Keterangan"), blank=True, null=True)

    def __str__(self) -> str:
        return self.nama_poli


class TenagaMedis(BaseModel):
    poliklinik = models.ManyToManyField(PoliKlinik, verbose_name=_("Poliklinik"))
    nama = models.CharField(_("Nama"), max_length=255)
    alamat = models.TextField(_("Alamat"), blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    no_hp = models.CharField(_("No HP"), max_length=255, blank=True, null=True)
    photo = models.ImageField(_("Photo"), upload_to='tenaga_medis/', blank=True, null=True)

    tahun_pengalaman = models.IntegerField(_("Tahun Pengalaman"), blank=True, null=True, default=0)
    tingakat_pendidikan = models.CharField(_("Tingkat Pendidikan"), max_length=255, blank=True, null=True)
    institusi = models.CharField(_("Institusi"), max_length=255, blank=True, null=True)
    tahun_lulus = models.IntegerField(_("Tahun Lulus"), blank=True, null=True, default=0)
    surat_izin_praktik = models.CharField(_("Surat Izin Praktik"), max_length=255, blank=True, null=True)
    catatan = models.TextField(_("Catatan"), blank=True, null=True)

    def __str__(self) -> str:
        return self.nama


class JadwalTenagaMedis(BaseModel):
    tenaga_medis = models.ForeignKey(TenagaMedis, verbose_name=_("Tenaga Medis"), on_delete=models.CASCADE)
    hari = models.CharField(_("Hari"), choices=Hari.choices, max_length=20)
    jam_mulai = models.TimeField(_("Jam Mulai"))
    jam_selesai = models.TimeField(_("Jam Selesai"))
    is_active = models.BooleanField(_("Status Aktif"), default=True)

    def __str__(self) -> str:
        return self.tenaga_medis.nama
