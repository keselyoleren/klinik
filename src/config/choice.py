from typing import Text
from django.db.models import TextChoices

class RoleUser(TextChoices):
    ADMIN = 'admin'
    DOKTER = 'dokter'
    USER = 'user'


class ThreadResult(TextChoices):
    OK = 'OK'
    ALREADY_RUN = 'ALREADY_RUN'
    ERROR = 'ERROR'
    INFO = 'INFO'

class JenisKelamin(TextChoices):
    LAKI_LAKI = 'LAKI-LAKI'
    PEREMPUAN = 'PEREMPUAN'

class StatusPasien(TextChoices):
    AKTIF = 'AKTIF'
    NONAKTIF = 'NONAKTIF'

class StatusRawatPasien(TextChoices):
    RESERVASI = 'RESERVASI'
    REGISTRASI = 'REGISTRASI'
    DIPERIKSA = 'DIPERIKSA'
    SELESAI = 'SELESAI'


class Hari(TextChoices):
    SENIN = 'SENIN'
    SELASA = 'SELASA'
    RABU = 'RABU'
    KAMIS = 'KAMIS'
    JUMAT = 'JUMAT'
    SABTU = 'SABTU'
    MINGGU = 'MINGGU'

class StatusPerokok(TextChoices):
    MEROKOK = 'MEROKOK'
    TIDAK_MEROKOK = 'TIDAK MEROKOK'

class StatusAlergi(TextChoices):
    YA = 'Ya'
    TIDAK = 'Tidak'

class CaraMasuk(TextChoices):
    URJ = 'URJ'
    UGD = 'UGD'
    LANGSUNG = 'Langsung'


class JenisKasus(TextChoices):
    KEBIDANAN = 'Kebidanan dan Penyakit Kandungan'
    KESEHATAN_ANAK = 'Kesehatan Anak'
    BEDAH = 'Bedah'
    PENYAKIT_DALAM = 'Penyakit Dalam'
    LAIN_LAIN = 'Lain - lain'

class StatusImunisasi(TextChoices):
    BCG = 'BCG'
    DPT = 'DPT'
    POLIO = 'Polio'
    MMR = 'MMR'
    TT = 'TT'

class StatusPeserta(TextChoices):
    BPJS = 'BPJS'
    UMUM = 'UMUM'
    JAMSOSTEK = 'JAMSOSTEK / PERUSAHAAN'
    
class UnitLayanan(TextChoices):
    RAWAT_JALAN = 'Rawat Jalan'
    RAWAT_INAP = 'Rawat Inap'
    FISIOTERAPI = 'Fisioterapi'
    LABORATORIUM = 'Laboratorium'

class KeadaanWaktuKeluar(TextChoices):
    SEMBUH = 'Sembuh'
    PERBAIKAN = 'Perbaikan'
    SAKIT = 'Sakit'
    MENINGGAL_KURANG = 'Meninggal setelah < 24 jam rawat'
    MENINGGAL_LEBIH = 'Meninggal setelah > 24 jam rawat'

class HasilRapidAntigen(TextChoices):
    NEGATIF = 'Negatif'
    POSITIF = 'Positif'

class StatusPersetujuan(TextChoices):
    PERSETUJUAN = 'Persetujuan'
    PENOLAKAN = 'Penolakan'

class StatusNarkoba(TextChoices):
    POSITIF = 'Positif'
    NEGATIF = 'Negatif'

class DitujukanChoice(TextChoices):
    DIRI_SENDIRI = 'Diri Sendiri'
    SUAMI = 'Suami'
    ISTRI = 'Istri'
    AYAH = 'Ayah'
    ANAK = 'Anak'
    IBU = 'Ibu'
    ORANG_LAIN = 'Orang Lain'

class YesOrNo(TextChoices):
    YA = 'YA'
    TIADK = 'TIDAK'

DAY_CODE = {
    Hari.MINGGU: 0,
    Hari.SENIN: 1,
    Hari.SELASA: 2,
    Hari.RABU: 3,
    Hari.KAMIS: 4,
    Hari.JUMAT: 5,
    Hari.SABTU: 6,    
}