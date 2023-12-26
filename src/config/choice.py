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
    RAWAT_JALAN = 'RAWAT JALAN'
    RAWAT_INAP = 'RAWAT INAP'
    AKTIF = 'AKTIF'
    NONAKTIF = 'NONAKTIF'

class StatusRawatJalan(TextChoices):
    RESERVASI = 'RESERVASI'
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

DAY_CODE = {
    Hari.MINGGU: 0,
    Hari.SENIN: 1,
    Hari.SELASA: 2,
    Hari.RABU: 3,
    Hari.KAMIS: 4,
    Hari.JUMAT: 5,
    Hari.SABTU: 6,    
}