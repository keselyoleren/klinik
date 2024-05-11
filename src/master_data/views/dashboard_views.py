# myapp/views.py

from django.views.generic import TemplateView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.choice import DAY_CODE
from master_data.models import *
from pasien.models import *


class InventoryObatListView(IsAuthenticated, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['total_pasien'] = Pasien.objects.count()
        context['pasien_rawat_jalan'] = RawatInap.objects.count()
        context['pasien_rawat_inap'] = RawatJalan.objects.count()
        context['pasien_fisioterapi'] = PasienFisioterapi.objects.count()
        context['tenaga_medis'] = TenagaMedis.objects.count()

        # jadwal
        context['header'] = 'Jadwal Tenaga Medis'
        context['header_title'] = 'Jadwal Tenaga Medis'
        context['jadwal'] = [
            {
                'title': f"{jadwal.tenaga_medis}",
                'hari': jadwal.hari,
                'code_hari': DAY_CODE.get(jadwal.hari, None),
                'duration': f"{jadwal.jam_mulai.strftime('%H:%M')} - {jadwal.jam_selesai.strftime('%H:%M')}",
                
            } for jadwal in JadwalTenagaMedis.objects.filter(is_active=True)
        ]
        return context
    