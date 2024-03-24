# myapp/views.py

from django.views.generic import TemplateView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
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


        return context
    