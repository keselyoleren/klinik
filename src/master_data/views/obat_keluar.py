# myapp/views.py

from ast import In
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from master_data.form.inventory_obat_form import InfentoryObatForm, ObatKeluarForm
from master_data.models import InventoryObat, ObatKeluar

class ObatKeluarListView(IsAuthenticated, ListView):
    model = ObatKeluar
    template_name = 'inventory_obat_keluar/list.html'
    context_object_name = 'obat_keluar'
    
    def get_obat(self):
        return InventoryObat.objects.get(id=self.kwargs['inv_obat_id'])

    def get_queryset(self):
        if self.kwargs.get('inv_obat_id'):
            return self.model.objects.filter(obat__id=self.kwargs['inv_obat_id'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat Keluar'
        context['header_title'] = 'List Inventory Obat Keluar'
        context['btn_add'] = True
        context['obat'] = self.get_obat()
        context['create_url'] = reverse_lazy('obat-keluar-create', kwargs={'inv_obat_id': self.kwargs['inv_obat_id']})
        return context

class ObatKeluarCreateView(IsAuthenticated, CreateView):
    model = ObatKeluar
    template_name = 'component/form.html'
    form_class = ObatKeluarForm

    def get_success_url(self) -> str:
        return reverse_lazy('obat-keluar-list', kwargs={'inv_obat_id': self.kwargs['inv_obat_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat Keluar'
        context['header_title'] = 'Tambah Inventory Obat Keluar'
        return context

    def form_valid(self, form):
        form.instance.obat = InventoryObat.objects.get(id=self.kwargs['inv_obat_id'])
        form.save()
        inv_obat = InventoryObat.objects.get(id=self.kwargs['inv_obat_id'])
        inv_obat.stok -= form.instance.jumlah
        inv_obat.save()
        return super().form_valid(form)

class ObatKeluarUpdateView(IsAuthenticated, UpdateView):
    model = ObatKeluar
    template_name = 'component/form.html'
    form_class = ObatKeluarForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('obat-keluar-list', kwargs={'inv_obat_id': self.get_object().obat.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventor Obat Keluar'
        context['header_title'] = 'Edit Inventory Obat Keluar'
        return context

    def form_valid(self, form):
        form.instance.obat = self.get_object().obat
        form.save()
        return super().form_valid(form)

class ObatKeluarDeleteView(IsAuthenticated, DeleteView):
    model = ObatKeluar
    template_name = 'component/delete.html'
    success_url = reverse_lazy('obat-keluar-list')

    def get_success_url(self) -> str:
        return reverse_lazy('obat-keluar-list', kwargs={'inv_obat_id': self.get_object().obat.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat Keluar'
        context['header_title'] = 'Delete Inventory Obat Keluar'
        return context
