from django.utils.translation import gettext as _
from config.choice import CaraMasuk, JenisKasus, JenisKelamin, StatusAlergi, StatusImunisasi, StatusPasien, StatusPerokok, StatusPeserta, StatusRawatPasien, KeadaanWaktuKeluar, UnitLayanan
from config.models import BaseModel
from django.db import models

# Create your models here.
class Pasien(BaseModel):
    nik = models.CharField(_("Nomor Kartu Identitas"), max_length=255)
    full_name = models.CharField(_("Nama Lengkap"), max_length=255)
    phone = models.CharField(_("No.Telepon"), max_length=255, blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True, null=True)
    tempat_lahir = models.CharField(_("Tempat Lahir"), max_length=255, blank=True, null=True)
    tanggal_lahir = models.DateField(_("Tanggal Lahir"), blank=True, null=True)
    jenis_kelamin = models.CharField(_("Jenis Kelamin"), max_length=255, choices=JenisKelamin.choices, blank=True, null=True)
    nama_ibu = models.CharField(_("Nama Ibu Kandung"), max_length=255, blank=True, null=True)
    
    agama = models.CharField(_("Agama"), max_length=255, blank=True, null=True)
    pekerjaan = models.CharField(_("Pekerjaan"), max_length=255, blank=True, null=True)
    alamat = models.TextField(_("Alamat Kartu Identitas"), blank=True, null=True)
    unit = models.TextField(_("Unit Layanan"), choices=UnitLayanan.choices, blank=True, null=True)
    status = models.CharField(_("Status"), max_length=255, choices=StatusPasien.choices, default=StatusPasien.AKTIF)
    
    

    def __str__(self) -> str:
        return self.full_name


class RawatJalan(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    dokter = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Dokter"), on_delete=models.CASCADE)
    waktu_konsultasi = models.DateTimeField(_("Waktu Konsultasi"), blank=True, null=True)
    status = models.CharField(_("Status"), max_length=255, choices=StatusRawatPasien.choices, default=StatusRawatPasien.REGISTRASI)

    def __str__(self) -> str:
        return self.pasien.full_name

class AssesmentRawatJalan(BaseModel):
    pasien_rawat_jalan = models.ForeignKey(RawatJalan, verbose_name=_("Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    alergi = models.CharField(_("Alergi"), max_length=255, blank=True, null=True, choices=StatusAlergi.choices)

    # skrining
    tinggi_badan = models.CharField(_("Tinggi Badan"), max_length=20, blank=True, null=True)
    berat_badan = models.CharField(_("Berat Badan"), max_length=20, blank=True, null=True)
    imt = models.CharField(_("IMT"), max_length=20, blank=True, null=True)

    # vital sign
    suhu_tubuh = models.CharField(_("Suhu Tubuh"), max_length=20, blank=True, null=True)
    nadi = models.CharField(_("Nadi"), max_length=20, blank=True, null=True)
    td = models.CharField(_("TD"), max_length=20, blank=True, null=True)
    rr = models.CharField(_("RR"), max_length=20, blank=True, null=True)

    # assesment
    riwayat_penhakit = models.CharField(_("Riwayat Penyakit"), max_length=255, blank=True, null=True)
    keluhan_utama = models.TextField(_("Keluhan Utama"), blank=True, null=True)
    obat = models.TextField(_("Obat-obatan"),  help_text="Obat-obatan yang sedang dikonsumsi dan/atau dibawa pasien saat ini", blank=True, null=True)
    pemerkiksaan = models.TextField(_("Pemeriksaan"), blank=True, null=True, help_text="Pemeriksaan Penunjang dan hasil yang sudah ada")

    # status general
    kondisi_umum = models.CharField(_("Kondisi Umum"), max_length=255, blank=True, null=True)

    # jantung
    inspeksi = models.CharField(_("Inspeksi"), max_length=255, blank=True, null=True)
    palpasi = models.CharField(_("Palpasi"), max_length=255, blank=True, null=True)
    perkusi = models.CharField(_("Perkusi"), max_length=255, blank=True, null=True)
    auskultasi = models.CharField(_("Auskultasi"), max_length=255, blank=True, null=True)

    # paru
    inspeksi_paru = models.CharField(_("Inspeksi"), max_length=255, blank=True, null=True)
    palpasi_paru = models.CharField(_("Palpasi"), max_length=255, blank=True, null=True)
    perkusi_paru = models.CharField(_("Perkusi"), max_length=255, blank=True, null=True)
    auskultasi_paru = models.CharField(_("Auskultasi"), max_length=255, blank=True, null=True)

    # status lokalis
    status_lokalis = models.CharField(_("Status Lokalis"), max_length=255, blank=True, null=True, help_text="(Pemeriksaan terkait keluhan saat ini)")

    informasi_tambahan = models.TextField(_("Informasi Tambahan"), blank=True, null=True)
    diagnosis = models.TextField(_("Diagnosis Kerja / Diagnosis Banding"), blank=True, null=True)
    instruksi_awal_dokter = models.TextField(_("Instruksi Awal Dokter"), blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Tenaga Medis"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.pasien_rawat_jalan.pasien.full_name



    

class RekamMedis(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Nama Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Tenaga Medis"), on_delete=models.CASCADE)
    keluhan_utama = models.TextField(_("Keluhan Utama"), blank=True, null=True)
    status_perokok = models.CharField(_("Status Perokok"), max_length=20, choices=StatusPerokok.choices, blank=True, null=True)
    riwayat_penyakit = models.CharField(_("Riwayat Penyakit"), max_length=255, blank=True, null=True)
    riwayat_alergi = models.CharField(_("Riwayat Alergi"), max_length=255, blank=True, null=True)
    suhu_tubuh = models.CharField(_("Suhu Tubuh"), max_length=255)
    nadi = models.CharField(_("Nadi"), max_length=20)
    sistole = models.CharField(_("Sistole"), max_length=20)
    diastole = models.CharField(_("Diastole"), max_length=20)
    frekuensi_pernafasan = models.CharField(_("Frekuensi Pernafasan"), max_length=20)
    tinggi_badan = models.CharField(_("Tinggi Badan"), max_length=20)
    berat_badan = models.CharField(_("Berat Badan"), max_length=20)
    imt = models.CharField(_("IMT"), max_length=20)


    def __str__(self) -> str:
        try:
            return self.pasien.full_name
        except:
            return ""

class RawatInap(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Nama Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    no_rm = models.CharField(_("No RM"), max_length=255)
    kelas = models.CharField(_("Kelas"), max_length=255)
    kelas = models.CharField(_("Kelas"), max_length=255)
    peserta = models.CharField(_("Peserta"), max_length=255, choices=StatusPeserta.choices, blank=True, null=True, help_text="Peserta BPJS / Umum")
    cara_masuk = models.CharField(_("Cara Masuk"), max_length=255, choices=CaraMasuk.choices)
    jenis_kasus = models.CharField(_("Jenis Kasus"), max_length=255, choices=JenisKasus.choices)
    tgl_masuk = models.DateTimeField(_("Tanggal Masuk"), null=True, blank=True)
    tgl_keluar = models.DateTimeField(_("Tanggal Keluar"), null=True, blank=True)
    lama_rawat = models.CharField(_("Lama Rawat"), max_length=100, blank=True, null=True)
    golongan_darah = models.CharField(_("Hasil PA / Golongan Darah"), max_length=100, blank=True, null=True)
    infeksi_nosokomial = models.CharField(_("Infeksi Nosokomial"), max_length=100, blank=True, null=True)
    diagnosis_masuk = models.TextField(_("Diagnosis Masuk"), max_length=100, blank=True, null=True)
    diagnosis_akhir = models.TextField(_("Diagnosis akhir"), max_length=100, blank=True, null=True)
    status_imunisasi = models.CharField(_("Status Imunisasi"), choices=StatusImunisasi.choices, blank=True, null=True, max_length=100)
    cara_keluar = models.CharField(_("Cara Keluar"), max_length=255, blank=True, null=True)
    keaddan_waktu_keluar = models.CharField(_("Keadaan Waktu Keluar"), choices=KeadaanWaktuKeluar.choices, max_length=100, blank=True, null=True)
    dokter = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Dokter yang Merawat"), on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        try:
            return self.pasien.full_name
        except Exception:
            return ""

class CatatanTerIntegrasi(BaseModel):
    pasien_rawat_jalan = models.ForeignKey(RawatJalan, verbose_name=_("Pasien Rawat Jalan"), on_delete=models.CASCADE, blank=True, null=True)
    pasien_rawat_inap = models.ForeignKey(RawatInap, verbose_name=_("Pasien Rawat inap"), on_delete=models.CASCADE, blank=True, null=True)
    catatan = models.TextField(_("Catatan"), help_text="Catatan Kemajuan, Rencana Tindakan dan Terapi", blank=True, null=True)
    profesi = models.CharField(_("Profesi"), max_length=255, blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Tenaga Medis"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        try:
            return self.pasien_rawat_jalan.pasien.full_name
        except:
            return self.pasien_rawat_inap.pasien.full_name


class Obat(BaseModel):
    pasien_rawat_inap = models.ForeignKey(RawatInap, verbose_name=_("Pasien Rawat Inap"), on_delete=models.CASCADE, blank=True, null=True)
    jenis_obat = models.CharField(_("Jenis Obat"), max_length=255, blank=True, null=True)
    nama = models.CharField(_("Nama Obat"), max_length=255, blank=True, null=True)
    jumblah = models.IntegerField(_("Jumblah"),  blank=True, null=True)
    harga = models.IntegerField(_("Harga"), blank=True, null=True)
    
    def __str__(self) -> str:
        return self.nama

class RincianBiaya(BaseModel):
    pasien_rawat_jalan = models.ForeignKey(RawatJalan, verbose_name=_("Pasien Rawat Jalan"), on_delete=models.CASCADE, blank=True, null=True)
    nama_layanan = models.CharField(_("Nama Layanan"), max_length=255, blank=True, null=True)
    harga = models.IntegerField(_("Harga"),  blank=True, null=True, help_text="Harga Layanan Rp.-")

    def __str__(self) -> str:
        return self.nama_layanan


class Resume(BaseModel):
    pasien_rawat_jalan = models.ForeignKey(RawatJalan, verbose_name=_("Pasien Rawat Jalan"), on_delete=models.CASCADE, blank=True, null=True)
    pasien_rawat_inap = models.ForeignKey(RawatInap, verbose_name=_("Pasien Rawat inap"), on_delete=models.CASCADE, blank=True, null=True)
    dignosis = models.CharField(_("Dignosis"), max_length=255, blank=True, null=True)
    terapi = models.CharField(_("Terapi / Tindakan"), max_length=255, blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Nama Tenaga Medis"), on_delete=models.CASCADE)

    def __str__(self):
        return self.dignosis
    

class PasienFisioterapi(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Nama Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(_("Status"), max_length=255, choices=StatusRawatPasien.choices, default=StatusRawatPasien.REGISTRASI)


    def __str__(self) -> str:
        return super().__str__()