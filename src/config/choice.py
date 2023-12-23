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