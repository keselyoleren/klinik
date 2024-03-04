from pyexpat import model
from statistics import mode
from django.db import models
from config.choice import DitujukanChoice, HasilRapidAntigen, JenisKelamin, StatusNarkoba
from config.models import BaseModel
from django.utils.translation import gettext as _
# Create your models here.

class KeteraganSakit(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    pasien = models.ForeignKey('pasien.Pasien', on_delete=models.CASCADE, blank=True, null=True)
    diangnosa = models.CharField(_('Diagnosa'), max_length=101, blank=True, null=True)
    start = models.DateField(_('Mulai'), blank=True, null=True)
    end = models.DateField(_('Sampai'), blank=True, null=True)
    

    def __str__(self) -> str:
        return self.pasien.full_name


class KeteranganSehat(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    pasien = models.ForeignKey('pasien.Pasien', on_delete=models.CASCADE, blank=True, null=True)
    tb = models.CharField(_('Tinggi Badan'), max_length=101, blank=True, null=True)
    bb = models.CharField(_('Berat Badan'), max_length=101, blank=True, null=True)
    suhu_tubuh = models.CharField(_('Suhu Tubuh'), max_length=101, blank=True, null=True)
    tes_buta_warna = models.CharField(_('Tes Buta Warna'), max_length=101, blank=True, null=True)
    golongan_darah = models.CharField(_('Golongan Darah'), max_length=101, blank=True, null=True)
    keperluan = models.CharField(_('Keperluan'), max_length=101, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien.full_name

class SuratRujukan(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    pasien = models.ForeignKey('pasien.Pasien', on_delete=models.CASCADE, blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', on_delete=models.CASCADE)
    keluhan = models.CharField(_('Keluhan'), max_length=101, blank=True, null=True)
    riwayat_penyakit = models.CharField(_('Riwayat Penyakit'), max_length=255, blank=True, null=True)
    t = models.CharField(_('T'), max_length=101, blank=True, null=True, help_text='oC')
    rr = models.CharField(_('RR'), max_length=101, blank=True, null=True, help_text='x/menit')
    nadi = models.CharField(_('Nadi'), max_length=101, blank=True, null=True, help_text='x/menit')
    tensi = models.CharField(_('Tensi'), max_length=101, blank=True, null=True, help_text='mmHg')
    hb = models.CharField(_('HB'), max_length=101, blank=True, null=True, help_text='g/dl')
    kesadaran = models.CharField(_('Kesadaran'), max_length=101, blank=True, null=True)
    diagnosa_sementara = models.CharField(_('Diagnosa Sementara'), max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien.full_name

class SuratKelahiran(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    nama_bayi = models.CharField(_('Nama Bayi'), max_length=101, blank=True, null=True)
    jenis_kelamin = models.CharField(_('Jenis Kelamin'), choices=JenisKelamin.choices, max_length=101, blank=True, null=True)
    panjang_badan = models.CharField(_('Panjang Badan'), max_length=101, blank=True, null=True)
    berat_badan = models.CharField(_('Berat Badan'), max_length=101, blank=True, null=True)
    hari = models.CharField(_('Hari'), max_length=101, blank=True, null=True)
    tanggal_lahir = models.DateField(_('Tanggal Lahir'), blank=True, null=True)
    jam = models.TimeField(_('Jam'), blank=True, null=True)
    tempat = models.CharField(_('Tempat'), max_length=101, blank=True, null=True)
    nama_ayah = models.CharField(_('Nama Ayah'), max_length=101, blank=True, null=True)
    nama_ibu = models.CharField(_('Nama Ibu'), max_length=101, blank=True, null=True)
    alamat = models.CharField(_('Alamat'), max_length=101, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien.full_name

class SuratKematian(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    pasien = models.ForeignKey('pasien.Pasien', on_delete=models.CASCADE, blank=True, null=True)
    tempat_kematian = models.CharField(_('Tempat Kematian'), max_length=101, blank=True, null=True)
    tanggal_kematian = models.DateField(_('Tanggal Kematian'), blank=True, null=True)
    sebab_kematian = models.CharField(_('Sebab Kematian'), max_length=101, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien.full_name

class SuratRapidAntigen(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    pasien = models.ForeignKey('pasien.Pasien', on_delete=models.CASCADE, blank=True, null=True)
    hasil = models.CharField(_('Hasil'), max_length=101, choices=HasilRapidAntigen.choices, blank=True, null=True)
    pemeriksaan = models.CharField(_('Pemeriksaan'), max_length=101,  blank=True, null=True)
    nilai_rujukan = models.CharField(_('Nilai Rujukan'), max_length=101, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.pasien.full_name


class SuratPerintahTugas(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', on_delete=models.CASCADE)
    dasar = models.CharField(_('Dasar'), max_length=101, blank=True, null=True)
    tujuan = models.CharField(_('Tujuan'), max_length=101, blank=True, null=True)

    def __str__(self) -> str:
        return self.tenaga_medis.nama


class SuratBebasNarkoba(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Yang Bertandatangan"), on_delete=models.CASCADE)
    pasien = models.ForeignKey('pasien.Pasien', verbose_name=_("Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    aphetamin = models.CharField(_('Aphetamin'), max_length=101, choices=StatusNarkoba.choices,  blank=True, null=True)
    methamphetamine = models.CharField(_('Methamphetamine'), max_length=101, choices=StatusNarkoba.choices, blank=True, null=True)
    thc = models.CharField(_('thc'), max_length=101, choices=StatusNarkoba.choices, blank=True, null=True)
    mor = models.CharField(_('Morphine'), max_length=101, choices=StatusNarkoba.choices, blank=True, null=True)
    keperluan = models.CharField(_('Keperluan'), max_length=101, blank=True, null=True)
    
    
    def __str__(self) -> str:
        return self.tenaga_medis.name


class SuratPersetujuan(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    # yang bertandatangan
    nama = models.CharField(_('Nama'), max_length=101, blank=True, null=True)
    umur = models.CharField(_('Umur'), max_length=101, blank=True, null=True)
    jenis_kelamin = models.CharField(_('Jenis Kelamin'), choices=JenisKelamin.choices, max_length=101, blank=True, null=True)
    
    tindakan_medik = models.CharField(_('Tindakan Medik'), max_length=101, blank=True, null=True)
    terhadap = models.CharField(_('Terhadap'), max_length=101, choices=DitujukanChoice.choices, blank=True, null=True)
    
    pasien = models.ForeignKey('pasien.Pasien', verbose_name=_("Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Tenaga Medis"), on_delete=models.CASCADE)
    tindakan_medik = models.CharField(_('Tindakan Medik'), max_length=101, blank=True, null=True)
    
    
    def __str__(self) -> str:
        return self.pasien.full_name

class SuratPenolakan(BaseModel):
    no = models.CharField(_('No'), max_length=101, blank=True, null=True)
    nama = models.CharField(_('Nama'), max_length=101, blank=True, null=True)
    umur = models.CharField(_('Umur'), max_length=101, blank=True, null=True)
    alamat = models.CharField(_('Alamat'), max_length=101, blank=True, null=True)
    phone = models.CharField(_('Telepon'), max_length=101, blank=True, null=True)
    jenis_kelamin = models.CharField(_('Jenis Kelamin'), choices=JenisKelamin.choices, max_length=101, blank=True, null=True)

    terhadap = models.CharField(_('Terhadap'), max_length=101, choices=DitujukanChoice.choices, blank=True, null=True)
    pasien = models.ForeignKey('pasien.Pasien', verbose_name=_("Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    diagnosa = models.CharField(_('Diagnosa'), max_length=101, blank=True, null=True)
    dirujuk = models.CharField(_('Menolak Dirujuk ke '), max_length=101, blank=True, null=True)


    def __str__(self) -> str:
        return self.pasien.full_name
