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
    no_rm = models.CharField(_("No Rekam Medis"), max_length=255, blank=True, null=True)
    
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
    jenis_alergi = models.CharField(_("Jenis Alergi"), max_length=255, blank=True, null=True)

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


class WongBaker(BaseModel):
    asses_rawat_jalan = models.ForeignKey(AssesmentRawatJalan, verbose_name=_("Asses Rawat Jalan"), on_delete=models.CASCADE, blank=True, null=True)
    interpretasi = models.CharField(_("Interpretasi Wong Baker"), max_length=255, blank=True, null=True)
    skor = models.CharField(_("Skor"), max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.interpretasi

class Vas(BaseModel):
    asses_rawat_jalan = models.ForeignKey(AssesmentRawatJalan, verbose_name=_("Asses Rawat Jalan"), on_delete=models.CASCADE, blank=True, null=True)
    interpretasi = models.CharField(_("Interpretasi Vas"), max_length=255, blank=True, null=True)
    skor = models.CharField(_("Skor"), max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.interpretasi

class Cpot(BaseModel):
    asses_rawat_jalan = models.ForeignKey(AssesmentRawatJalan, verbose_name=_("Asses Rawat Jalan"), on_delete=models.CASCADE, blank=True, null=True)
    interpretasi = models.CharField(_("Interpretasi Cpot"), max_length=255, blank=True, null=True)
    skor = models.CharField(_("Skor"), max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.interpretasi

class Gcs(BaseModel):
    asses_rawat_jalan = models.ForeignKey(AssesmentRawatJalan, verbose_name=_("Asses Rawat Jalan"), on_delete=models.CASCADE, blank=True, null=True)
    interpretasi = models.CharField(_("Interpretasi Gcs"), max_length=255, blank=True, null=True)
    skor = models.CharField(_("Skor"), max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.interpretasi


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

class PermintaanLabor(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Pasien"), on_delete=models.CASCADE, blank=True, null=True)
    
    # HEMATOLOGI
    hemoglobin = models.BooleanField(default=False, verbose_name="Hemoglobin")
    led = models.BooleanField(default=False, verbose_name="LED")
    leukosit = models.BooleanField(default=False, verbose_name="Leukosit")
    diff = models.BooleanField(default=False, verbose_name="Diff")
    bas = models.BooleanField(default=False, verbose_name="BAS")
    eos = models.BooleanField(default=False, verbose_name="EOS")
    stb = models.BooleanField(default=False, verbose_name="STB")
    seg = models.BooleanField(default=False, verbose_name="SEG")
    lim = models.BooleanField(default=False, verbose_name="LIM")
    mon = models.BooleanField(default=False, verbose_name="MON")
    trombosit = models.BooleanField(default=False, verbose_name="Trombosit")
    eritrosit = models.BooleanField(default=False, verbose_name="Eritrosit")
    hematokrit = models.BooleanField(default=False, verbose_name="Hematokrit")
    golongan_darah = models.BooleanField(default=False, verbose_name="Golongan Darah")
    clotting_time = models.BooleanField(default=False, verbose_name="Clotting Time")
    bleeding_time = models.BooleanField(default=False, verbose_name="Bleeding Time")
    mcv = models.BooleanField(default=False, verbose_name="MCV")
    mch = models.BooleanField(default=False, verbose_name="MCH")
    mchc = models.BooleanField(default=False, verbose_name="MCHC")

    # BIOKIMIA
    profil_diabetik = models.BooleanField(default=False, verbose_name="Profil Diabetik")
    gd_puasa = models.BooleanField(default=False, verbose_name="GD Puasa")
    gd_2_j_pp = models.BooleanField(default=False, verbose_name="GD 2 J PP")
    gd_sewaktu = models.BooleanField(default=False, verbose_name="GD Sewaktu")
    hba1c = models.BooleanField(default=False, verbose_name="HbA1C")
    kolesterol_total = models.BooleanField(default=False, verbose_name="Kolesterol Total")
    hdl_kolesterol = models.BooleanField(default=False, verbose_name="HDL Kolesterol")
    ldl_kolesterol = models.BooleanField(default=False, verbose_name="LDL Kolesterol")
    trigliserida = models.BooleanField(default=False, verbose_name="Trigliserida")
    bilirubin_total = models.BooleanField(default=False, verbose_name="Bilirubin Total")
    bilirubin_direk = models.BooleanField(default=False, verbose_name="Bilirubin Direk")
    bilirubin_indirek = models.BooleanField(default=False, verbose_name="Bilirubin Indirek")
    sgot = models.BooleanField(default=False, verbose_name="SGOT")
    sgpt = models.BooleanField(default=False, verbose_name="SGPT")
    alkasi_phospatashe = models.BooleanField(default=False, verbose_name="Alkasi Phospatashe")
    asam_urat = models.BooleanField(default=False, verbose_name="Asam Urat")
    ureum = models.BooleanField(default=False, verbose_name="Ureum")
    creatinin = models.BooleanField(default=False, verbose_name="Creatinin")
    bun = models.BooleanField(default=False, verbose_name="BUN")
    albumin = models.BooleanField(default=False, verbose_name="Albumin")
    total_protein = models.BooleanField(default=False, verbose_name="Total Protein")
    globulin = models.BooleanField(default=False, verbose_name="Globulin")
    ck_mb = models.BooleanField(default=False, verbose_name="CK_MB")
    
    # napza
    napza_cocaine = models.BooleanField(default=False, verbose_name="Cocaine (COC)")
    napza_metamphetamine = models.BooleanField(default=False, verbose_name="Metamphetamine (MET)")
    napza_cannabis = models.BooleanField(default=False, verbose_name="Cannabis (THC)")
    napza_o_morphine = models.BooleanField(default=False, verbose_name="O Morphine (MOR)")

    # ELEKTROLIT\
    elektrolit_cocaine = models.BooleanField(default=False, verbose_name="Cocaine (COC)")
    elektrolit_metamphetamine = models.BooleanField(default=False, verbose_name="Metamphetamine (MET)")
    elektrolit_cannabis = models.BooleanField(default=False, verbose_name="Cannabis (THC)")
    elektrolit_o_morphine = models.BooleanField(default=False, verbose_name="O Morphine (MOR)")

    # WDAL
    s_typhosa = models.BooleanField(default=False, verbose_name="S.Typhosa")
    s_typhosa_a = models.BooleanField(default=False, verbose_name="S.Typhosa A")
    s_typhosa_b = models.BooleanField(default=False, verbose_name="S.Typhosa B")
    s_typhosa_c = models.BooleanField(default=False, verbose_name="S.Typhosa C")
    
    # urine rutin
    makroskopis_urin = models.BooleanField(default=False, verbose_name="Makroskopis")
    warna_urin = models.BooleanField(default=False, verbose_name="Warna")
    kekeruhan = models.BooleanField(default=False, verbose_name="Kekeruhan")
    keasaman_ph = models.BooleanField(default=False, verbose_name="Keasaman/pH")
    berat_jenis = models.BooleanField(default=False, verbose_name="Berat Jenis")
    keton = models.BooleanField(default=False, verbose_name="Keton")
    darah_rutin = models.BooleanField(default=False, verbose_name="Darah")
    nitrit = models.BooleanField(default=False, verbose_name="Nitrit")
    kimiawi_urin = models.BooleanField(default=False, verbose_name="Kimiawi")
    protein_albumin = models.BooleanField(default=False, verbose_name="Protein (Albumin)")
    glukosa_reduksi = models.BooleanField(default=False, verbose_name="Glukosa (reduksi)")
    bilirubin = models.BooleanField(default=False, verbose_name="Bilirubin")
    urobilin = models.BooleanField(default=False, verbose_name="Urobilin")
    mikroskopis_urin = models.BooleanField(default=False, verbose_name="Mikroskopis")
    leukosit = models.BooleanField(default=False, verbose_name="Leukosit")
    eritrosit = models.BooleanField(default=False, verbose_name="Eritrosit")
    ephitel = models.BooleanField(default=False, verbose_name="Ephitel")
    kristal = models.BooleanField(default=False, verbose_name="Kristal")
    silinder = models.BooleanField(default=False, verbose_name="Silinder")
    lain_lain_urin_rutin = models.BooleanField(default=False, verbose_name="Lain-lain")

    # faces
    makroskopis_faces = models.BooleanField(default=False, verbose_name="Makroskopis")
    konsistensi = models.BooleanField(default=False, verbose_name="Konsistensi")
    warna_faces = models.BooleanField(default=False, verbose_name="Warna")
    bau = models.BooleanField(default=False, verbose_name="Bau")
    nanah = models.BooleanField(default=False, verbose_name="Nanah")
    darah_faces = models.BooleanField(default=False, verbose_name="Darah")
    kimiawi_faces = models.BooleanField(default=False, verbose_name="Kimiawi")
    benzidine_test = models.BooleanField(default=False, verbose_name="Benzidine Test")
    mikroskopis_faces = models.BooleanField(default=False, verbose_name="Mikroskopis")
    telur_cacing = models.BooleanField(default=False, verbose_name="Telur Cacing")
    sel_darah = models.BooleanField(default=False, verbose_name="Sel Darah")
    amoeba = models.BooleanField(default=False, verbose_name="Amoeba")
    lain_lain_faces = models.BooleanField(default=False, verbose_name="Lain-lain")

    # sputum
    sputum_bta_ct = models.BooleanField(default=False, verbose_name="Sputum BTA/CT")
    
    # mikrobiologi_parasitologi
    malaria = models.BooleanField(default=False, verbose_name="Malaria")
    
    # serologi 
    pp_test = models.BooleanField(default=False, verbose_name="PP Test")
    cek_rapid_test = models.BooleanField(default=False, verbose_name="Cek Rapid Test")
    cek_antigen = models.BooleanField(default=False, verbose_name="Cek Antigen")
    hcv = models.BooleanField(default=False, verbose_name="HCV")
    hbs_ag = models.BooleanField(default=False, verbose_name="HBs Ag")
    hiv_aids = models.BooleanField(default=False, verbose_name="HIV/AIDS")
    asto = models.BooleanField(default=False, verbose_name="Asto")
    dhf_test = models.BooleanField(default=False, verbose_name="DHF Test")
    anti_malaria_ict_test = models.BooleanField(default=False, verbose_name="Anti Malaria ICT Test")
    anti_dengue_igm = models.BooleanField(default=False, verbose_name="Anti Dengue Ig.M")
    anti_dengue_igg = models.BooleanField(default=False, verbose_name="Anti Dengue Ig.G")
    ns1ag_dengue = models.BooleanField(default=False, verbose_name="NS1Ag Dengue")
    anti_syphilis_igg_igm = models.BooleanField(default=False, verbose_name="Anti Syphilis Ig.G / Ig.M")
    igg_m_anti_salmonella_typhi_tubex = models.BooleanField(default=False, verbose_name="Ig.G/M Anti Salmonella Typhi / Tubex")

    catatan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Catatan")
    ket_lain_lain_faces = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lain lain faces")
    ket_lain_lain_urinte = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lain lain urin rutin")
    
    
    dokter_pengirim = models.ForeignKey('master_data.TenagaMedis', on_delete=models.CASCADE, verbose_name="Dokter Pengirim", blank=True, null=True)
    # tanggal_kirim = models.DateTimeField(verbose_name="Tanggal & jam", blank=True, null=True)
    # tgl_kirim = models.DateTimeField(verbose_name="Tanggal & jam", blank=True, null=True)
    kirim_tanggal = models.DateTimeField(verbose_name="Tanggal & jam", blank=True, null=True)
    
    ruangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ruang / Poli")
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="No. Telphone")
    ket_klinis = models.TextField(blank=True, null=True, verbose_name="Keterangan Klinis")

    spes_lab_diterima = models.DateTimeField(verbose_name="Spesimen Lab Diterima", blank=True, null=True)

    leukosit_hematologi = models.BooleanField(default=False, verbose_name="Leukosit")
    
class PermintaanLabor2(BaseModel):
    pasien = models.ForeignKey(Pasien, verbose_name=_("Pasien"), on_delete=models.CASCADE, blank=True, null=True)
   
    led = models.CharField(max_length=100, verbose_name="LED", help_text="Pria Wanita < 10 mm/jam < 15 mm/jam", blank=True, null=True)
    hemoglobin = models.CharField(max_length=100, verbose_name="Hemoglobin", help_text="Pria Wanita 13 - 16 gr/dl 12 - 14 gr/dl", blank=True, null=True)
    leukosit_hematologi = models.CharField(max_length=100, verbose_name="Leukosit", help_text="5.000 – 10.000 ribu/mm3", blank=True, null=True)
    # diff
    bas = models.CharField(max_length=100, verbose_name="BAS", help_text="0 - 1 %", blank=True, null=True)
    eos = models.CharField(max_length=100, verbose_name="EOS", help_text="1 - 3 %", blank=True, null=True)
    stb = models.CharField(max_length=100, verbose_name="STB", help_text="0 - 6 %", blank=True, null=True)
    seg = models.CharField(max_length=100, verbose_name="SEG", help_text="50 - 70 %", blank=True, null=True)
    lim = models.CharField(max_length=100, verbose_name="LIM", help_text="20 - 40 %", blank=True, null=True)
    mon = models.CharField(max_length=100, verbose_name="MON", help_text="2 - 3 %", blank=True, null=True)
    
    trombosit = models.CharField(max_length=100, verbose_name="Trombosit", help_text="150 s/d 500 ribu/mm3",blank=True, null=True)
    eritrosit_hematlogi = models.CharField(max_length=100, verbose_name="Eritrosit", help_text="4,0 - 5,0 juta/mm3",blank=True, null=True)
    hematokrit = models.CharField(max_length=100, verbose_name="Hematokrit", help_text="Pria Wanita 40 - 48 voc %37 – 43 voc %", blank=True, null=True)
    golongan_darah = models.CharField(max_length=100, verbose_name="Golongan Darah", help_text="A / B / AB / O", blank=True, null=True)
    clotting_time = models.CharField(max_length=100, verbose_name="Clotting Time", help_text="6 – 12 menit",blank=True, null=True)
    bleeding_time = models.CharField(max_length=100, verbose_name="Bleeding Time", help_text="1 - 6 Menit",blank=True, null=True)
    mcv = models.CharField(max_length=100, verbose_name="MCV", help_text="83,9 – 99,1 fl",blank=True, null=True)
    mch = models.CharField(max_length=100, verbose_name="MCH", help_text="27,8 – 33,8 pg",blank=True, null=True)
    mchc = models.CharField(max_length=100, verbose_name="MCHC", help_text="32,0 – 35,5 g/dl",blank=True, null=True)

    # biokimia
    gd_puasa = models.CharField(max_length=100, verbose_name="GD Puasa", help_text="50 - 100 mg/dl", blank=True, null=True)
    gd_2_j_pp = models.CharField(max_length=100, verbose_name="GD 2 J PP", help_text="80 - 125 mg/dl", blank=True, null=True)
    gd_sewaktu = models.CharField(max_length=100, verbose_name="GD Sewaktu", help_text="80 - 120 mg/dl", blank=True, null=True)
    hba1c = models.CharField(max_length=100, verbose_name="HbA1C", help_text="4,5 - 6 %", blank=True, null=True)
    kolesterol_total = models.CharField(max_length=100, verbose_name="Kolesterol Total", help_text="140-200 mg/dl", blank=True, null=True)
    hdl_kolesterol = models.CharField(max_length=100, verbose_name="HDL Kolesterol", help_text="33,0 – 49,4 mg/dl", blank=True, null=True)
    ldl_kolesterol = models.CharField(max_length=100, verbose_name="LDL Kolesterol", help_text="< 130 mg/dl", blank=True, null=True)
    trigliserida = models.CharField(max_length=100, verbose_name="Trigliserida", help_text="124 - 178 mg/dl", blank=True, null=True)
    bilirubin_total = models.CharField(max_length=100, verbose_name="Bilirubin Total", help_text="1,14 – 1,94 mg/dl", blank=True, null=True)
    bilirubin_direk = models.CharField(max_length=100, verbose_name="Bilirubin Direk", help_text="0,90 – 1,54 mg/dl", blank=True, null=True)
    bilirubin_indirek = models.CharField(max_length=100, verbose_name="Bilirubin Indirek", help_text="1,00 mg/dl", blank=True, null=True)
    sgot = models.CharField(max_length=100, verbose_name="SGOT", help_text="22,3 – 35,5 U/L", blank=True, null=True)
    sgpt = models.CharField(max_length=100, verbose_name="SGPT", help_text="24,5 – 39.2 U/L", blank=True, null=True)
    alkasi_phospatashe = models.CharField(max_length=100, verbose_name="Alkasi Phospatashe", help_text="15 – 112 U", blank=True, null=True)
    asam_urat = models.CharField(max_length=100, verbose_name="Asam Urat", help_text="Pria 3,4 – 7,2 mg/dl Wanita 2,1 – 5,7 mg/d, blank=True, null=Truel", blank=True, null=True)
    ureum = models.CharField(max_length=100, verbose_name="Ureum", help_text="46,9 - 73 mg/dl", blank=True, null=True)
    creatinin = models.CharField(max_length=100, verbose_name="Creatinin", help_text="0,9 – 1,2 mg/dl", blank=True, null=True)
    bun = models.CharField(max_length=100, verbose_name="BUN", help_text="8 – 20 mg/dl", blank=True, null=True)
    albumin = models.CharField(max_length=100, verbose_name="Albumin", help_text="2,57 – 4,11 mg/dl", blank=True, null=True)
    total_protein = models.CharField(max_length=100, verbose_name="Total Protein", help_text="4,49 – 5,61 mg/dl", blank=True, null=True)
    globulin = models.CharField(max_length=100, verbose_name="Globulin", help_text="2 - 3 gr/100 ml", blank=True, null=True)
    ck_mb = models.CharField(max_length=100, verbose_name="CK_MB", help_text="s/d 24 UL", blank=True, null=True)


    # napaza
    napza_cocaine = models.CharField(max_length=100, verbose_name="Cocaine (COC)", help_text="Negatif (-)", blank=True, null=True)
    napza_metamphetamine = models.CharField(max_length=100, verbose_name="Metamphetamine (MET)", help_text="Negatif (-)", blank=True, null=True)
    napza_cannabis = models.CharField(max_length=100, verbose_name="Cannabis (THC)", help_text="Negatif (-)", blank=True, null=True)
    napza_o_morphine = models.CharField(max_length=100, verbose_name="Morphine (MOR)", help_text="Negatif (-)", blank=True, null=True)

    # ELEKTROLIT\
    k = models.CharField(max_length=100, blank=True, null=True, verbose_name="K", help_text="3,5 – 5,5 mmol/L")
    na = models.CharField(max_length=100, blank=True, null=True, verbose_name="NA", help_text="135 – 145 mmol/L")
    ci = models.CharField(max_length=100, blank=True, null=True, verbose_name="CI", help_text="98 – 108 mmol/L")
    ca = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ca", help_text="")
    ph = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ph", help_text="")

    # WDAL
    s_typhosa = models.CharField(max_length=100, blank=True, null=True, verbose_name="S.Typhosa")
    s_typhosa_a = models.CharField(max_length=100, blank=True, null=True, verbose_name="S.Typhosa A")
    s_typhosa_b = models.CharField(max_length=100, blank=True, null=True, verbose_name="S.Typhosa B")
    s_typhosa_c = models.CharField(max_length=100, blank=True, null=True, verbose_name="S.Typhosa C")

    # makroskopis_urin = models.BooleanField(default=False, verbose_name="Makroskopis")
    warna_urin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Warna", help_text="Kuning Muda")
    kekeruhan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kekeruhan", help_text="Jernih")
    keasaman_ph = models.CharField(max_length=100, blank=True, null=True, verbose_name="Keasaman/pH", help_text="4 - 7.5")
    berat_jenis = models.CharField(max_length=100, blank=True, null=True, verbose_name="Berat Jenis", help_text="1002 - 1030")
    keton = models.CharField(max_length=100, blank=True, null=True, verbose_name="Keton", help_text="Negatif")
    darah_rutin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Darah", help_text="Negatif")
    nitrit = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nitrit", help_text="Negatif")
    # kimiawi_urin = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kimiawi", help_text="")
    protein_albumin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Protein (Albumin)", help_text="Negatif")
    glukosa_reduksi = models.CharField(max_length=100, blank=True, null=True, verbose_name="Glukosa (reduksi)", help_text="Negatif")
    bilirubin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bilirubin", help_text="Negatif")
    urobilin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Urobilin", help_text="0,1 – 1 mg/dl")
    # mikroskopis_urin = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mikroskopis", help_text="")
    leukosit = models.CharField(max_length=100, blank=True, null=True, verbose_name="Leukosit", help_text="< 6 / LPB")
    eritrosit = models.CharField(max_length=100, blank=True, null=True, verbose_name="Eritrosit", help_text="0 – 1 / LPB")
    ephitel = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ephitel", help_text="Positif")
    kristal = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kristal", help_text="Negatif")
    silinder = models.CharField(max_length=100, blank=True, null=True, verbose_name="Silinder", help_text="Negatif")
    lain_lain_urin_rutin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lain-lain", help_text="")

    # faces
    # makroskopis_faces = models.CharField(max_length=255,blank=True, null=True, verbose_name="Makroskopis")
    konsistensi = models.CharField(max_length=100,blank=True, null=True, verbose_name="Konsistensi", help_text="Lunak dan Berbentuk")
    warna_faces = models.CharField(max_length=100,blank=True, null=True, verbose_name="Warna", help_text="Coklat Muda")
    bau = models.CharField(max_length=100,blank=True, null=True, verbose_name="Bau", help_text="Bau indol, skatol")
    nanah = models.CharField(max_length=100,blank=True, null=True, verbose_name="Nanah", help_text="Negatif")
    darah_faces = models.CharField(max_length=100,blank=True, null=True, verbose_name="Darah", help_text="Negatif")
    # kimiawi_faces = models.CharField(max_length=255,blank=True, null=True, verbose_name="Kimiawi", help_text="")
    benzidine_test = models.CharField(max_length=100,blank=True, null=True, verbose_name="Benzidine Test", help_text="Negatif")
    # mikroskopis_faces = models.CharField(max_length=255,blank=True, null=True, verbose_name="Mikroskopis", help_text="")
    telur_cacing = models.CharField(max_length=100,blank=True, null=True, verbose_name="Telur Cacing", help_text="Negatif")
    sel_darah = models.CharField(max_length=100,blank=True, null=True, verbose_name="Sel Darah", help_text="Negatif")
    amoeba = models.CharField(max_length=100,blank=True, null=True, verbose_name="Amoeba", help_text="Negatif")
    lain_lain_faces = models.CharField(max_length=100,blank=True, null=True, verbose_name="Lain-lain")

    # sputum
    sputum_bta_ct = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sputum BTA/CT")
    
    # mikrobiologi_parasitologi
    malaria = models.CharField(max_length=100, blank=True, null=True, verbose_name="Malaria")
    
    # serologi 
    pp_test = models.CharField(max_length=100, blank=True, null=True, verbose_name="PP Test", help_text="")
    cek_rapid_test = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cek Rapid Test", help_text="")
    cek_antigen = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cek Antigen", help_text="")
    hcv = models.CharField(max_length=100, blank=True, null=True, verbose_name="HCV", help_text="")
    hbs_ag = models.CharField(max_length=100, blank=True, null=True, verbose_name="HBs Ag", help_text="Non Reaktif")
    anti_hbs = models.CharField(max_length=100, blank=True, null=True, verbose_name="Anti HBs", help_text="Negatif : < 8 mIU/mL Intermediate : 8 – 12 Positif : > 12")
    hiv_aids = models.CharField(max_length=100, blank=True, null=True, verbose_name="HIV/AIDS", help_text="")
    asto = models.CharField(max_length=100, blank=True, null=True, verbose_name="Asto", help_text="")
    dhf_test = models.CharField(max_length=100, blank=True, null=True, verbose_name="DHF Test", help_text="")
    anti_malaria_ict_test = models.CharField(max_length=100, blank=True, null=True, verbose_name="Anti Malaria ICT Test", help_text="")
    anti_dengue_igm = models.CharField(max_length=100, blank=True, null=True, verbose_name="Anti Dengue Ig.M", help_text="")
    anti_dengue_igg = models.CharField(max_length=100, blank=True, null=True, verbose_name="Anti Dengue Ig.G", help_text="")
    ns1ag_dengue = models.CharField(max_length=100, blank=True, null=True, verbose_name="NS1Ag Dengue", help_text="")
    anti_syphilis_igg_igm = models.CharField(max_length=100, blank=True, null=True, verbose_name="Anti Syphilis Ig.G / Ig.M", help_text="")
    igg_m_anti_salmonella_typhi_tubex = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ig.G/M Anti Salmonella Typhi / Tubex", help_text="0-2 : Negatif 3 : Borderline 4-10 : Positif")

    permintaan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Permintaan", help_text="")
    pemeriksa = models.ForeignKey('master_data.TenagaMedis', on_delete=models.CASCADE, verbose_name="Pemeriksa", blank=True, null=True)