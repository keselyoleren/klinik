from django.utils.translation import gettext as _
from config.choice import CaraMasuk, JenisKasus, JenisKelamin, StatusAlergi, StatusImunisasi, StatusPasien, StatusPerokok, StatusPersetujuan, StatusPeserta, StatusRawatPasien, KeadaanWaktuKeluar, UnitLayanan
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
        return self.pasien.full_name

class AssesMentFisioTerapi(BaseModel):
    pasien_fisioterapi = models.ForeignKey(PasienFisioterapi, verbose_name=_("Pasien Fisioterapi"), on_delete=models.CASCADE, blank=True, null=True)

    # Annamanse
    keluhan_utama = models.CharField(_("Keluhan Utama"), max_length=255, blank=True, null=True)
    riwayat_penyakit_sekarang = models.TextField(_("Riwayat Penyakit Sekarang"), blank=True, null=True)
    riwayat_penyakit_dahulu = models.TextField(_("Riwayat Penyakit Dahulu"), blank=True, null=True)

    # Pemeriksaan Fisik
    # tanda vital
    td = models.CharField(_("TD"), max_length=255, blank=True, null=True)
    hr = models.CharField(_("HR"), max_length=255, blank=True, null=True)
    suhu = models.CharField(_("Suhu"), max_length=255, blank=True, null=True)
    rr = models.CharField(_("RR"), max_length=255, blank=True, null=True)
    pr = models.CharField(_("PR"), max_length=255, blank=True, null=True)
    sekor_nyeri = models.CharField(_("Sekor Nyeri"), max_length=255, blank=True, null=True)

    # kemampuan fungsi
    alat_bantu = models.CharField(_("Alat Bantu"), max_length=255, blank=True, null=True)
    prothese = models.CharField(_("Prothese"), max_length=255, blank=True, null=True)
    deformitas = models.CharField(_("Deformitas"), max_length=255, blank=True, null=True)
    resiko_jatuh = models.CharField(_("Resiko Jatuh"), max_length=255, blank=True, null=True)
    lain_lain = models.CharField(_("Lain Lain"), max_length=255, blank=True, null=True)

    # pemeriksaan sistemik khusus
    muscoloskeletal = models.CharField(_("Muscoloskeletal"), max_length=255, blank=True, null=True)
    neoromuscular = models.CharField(_("Neoromuscular"), max_length=255, blank=True, null=True)
    cardiopulmonal  = models.CharField(_("Cardiopulmonal"), max_length=255, blank=True, null=True)
    integument = models.CharField(_("Integument"), max_length=255, blank=True, null=True)

    # pengukuran khususu 
    mes_muscoloskeletal = models.CharField(_("Muscoloskeletal"), max_length=255, blank=True, null=True)
    mes_neoromuscular = models.CharField(_("Neoromuscular"), max_length=255, blank=True, null=True)
    mes_cardiopulmonal  = models.CharField(_("Cardiopulmonal"), max_length=255, blank=True, null=True)
    mes_integument = models.CharField(_("Integument"), max_length=255, blank=True, null=True)

    # data penunjang
    radiologi = models.CharField(_("Radiologi"), max_length=255, blank=True, null=True)
    emg = models.CharField(_("EMG"), max_length=255, blank=True, null=True)
    laboratorium = models.CharField(_("Laboratorium"), max_length=255, blank=True, null=True)
    lain_lain = models.CharField(_("Lain Lain"), max_length=255, blank=True, null=True)

    # diagnosis fisioterapi
    diagnosis_fisioterapi = models.CharField(_("Diagnosis Fisioterapi"), max_length=255, blank=True, null=True)

    # program rencana terapi
    program_rencana_terapi = models.CharField(_("Program Rencana Terapi"), max_length=255, blank=True, null=True)

    # evaluasi
    evaluasi = models.CharField(_("Evaluasi"), max_length=255, blank=True, null=True)

    # fisioterapis
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Fisioterapis"), on_delete=models.CASCADE, blank=True, null=True)

    
    def __str__(self) -> str:
        return self.pasien_fisioterapi.pasien.full_name

class Intervensi(BaseModel):
    asses_fisioterapi = models.ForeignKey(AssesMentFisioTerapi, verbose_name=_("Asses Fisioterapi"), on_delete=models.CASCADE, blank=True, null=True)
    intervensi = models.CharField(_("Intervensi"), max_length=255, blank=True, null=True)
    tempat_yang_diterapi = models.CharField(_("Tempat / area Yang Diterapi"), max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.intervensi


class RujukanKeluar(BaseModel):
    pasien_fisioterapi = models.ForeignKey(PasienFisioterapi, verbose_name=_("Pasien Fisioterapi"), on_delete=models.CASCADE, blank=True, null=True)
    hasil_pemeriksaan_awal = models.TextField(_("Hasil Pemeriksaan Awal"), blank=True, null=True)
    diagnosis_medis = models.TextField(_("Diagnosis Medis"), blank=True, null=True)
    diagnosis_fisioterapi = models.TextField(_("Diagnosis Fisioterapi"), blank=True, null=True) 
    tindakan = models.TextField(_("Tindakan/terapi yg telah dilakukan"), blank=True, null=True)
    evaluasi = models.TextField(_("Evaluasi"), blank=True, null=True)   
    rekomendasi = models.TextField(_("Rekomendasi / Ulasan"), blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Fisioterapis perujuk"), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien_fisioterapi.pasien.full_name

class ResumeFisioterapi(BaseModel):
    pasien_fisioterapi = models.ForeignKey(PasienFisioterapi, verbose_name=_("Pasien Fisioterapi"), on_delete=models.CASCADE, blank=True, null=True)
    diagnosis_medis = models.TextField(_("Diagnosis Medis"), blank=True, null=True)
    tujuan_rujukan = models.TextField(_("Tujuan Rujukan"), blank=True, null=True)

    # kondisi awal
    gejala = models.CharField(_("Gejala / sindroma"), max_length=255, blank=True, null=True)
    gerak_fungsional = models.CharField(_("Status gangguan gerak fungsional/ Parameter"), max_length=255, blank=True, null=True)
    diagnosis_fisioterapi = models.TextField(_("Diagnosis Fisioterapi"), blank=True, null=True) 
    
    # kondisi akhir
    gejala_end = models.CharField(_("Gejala / sindroma"), max_length=255, blank=True, null=True)
    gerak_fungsional_end = models.CharField(_("Status gangguan gerak fungsional/ Parameter"), max_length=255, blank=True, null=True)
    diagnosis_fisioterapi_end = models.TextField(_("Diagnosis Fisioterapi"), blank=True, null=True) 
    
    hambatan = models.CharField(_("Hambatan keberhasilan"), max_length=255, blank=True, null=True)
    tindak_lanjut = models.CharField(_("Rekomendasi tindak lanjut"), max_length=255, blank=True, null=True)
    
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Fisioterapis"), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien_fisioterapi.pasien.full_name


class MonitoringFisoterapi(BaseModel):
    pasien_fisioterapi = models.ForeignKey(PasienFisioterapi, verbose_name=_("Pasien Fisioterapi"), on_delete=models.CASCADE, blank=True, null=True)
    tindakan = models.CharField(_("Tindakan"), max_length=255, blank=True, null=True)
    perkembangan =  models.TextField(_("Perkembangan (S=Subyektif; O=Obyektif; A=Asesmen; R=Rencana.)"), blank=True, null=True)
    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Fisioterapis"), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien_fisioterapi.pasien.full_name


class InformedConsent(BaseModel):
    pasien_fisioterapi = models.ForeignKey(PasienFisioterapi, verbose_name=_("Pasien Fisioterapi"), on_delete=models.CASCADE, blank=True, null=True)
    ruang = models.CharField(_("Ruang / Kamar"), max_length=255, blank=True, null=True)
    # yang bertanggung jawab
    nama = models.CharField(_("Nama"), max_length=255, blank=True, null=True)
    umur = models.CharField(_("Umur"), max_length=255, blank=True, null=True)
    jenis_kelamin = models.CharField(_("Jenis Kelamin"), choices=JenisKelamin.choices, max_length=255, blank=True, null=True)

    status_persetujuan = models.CharField(_("Status Persetujuan"), choices=StatusPersetujuan.choices, max_length=255, blank=True, null=True)

    tenaga_medis = models.ForeignKey('master_data.TenagaMedis', verbose_name=_("Fisioterapis"), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.pasien_fisioterapi.pasien.full_name