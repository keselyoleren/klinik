# myapp/views.py
from django.db import models

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from master_data.form.inventory_obat_form import InfentoryObatForm
from master_data.models import InventoryObat, ObatKeluar, ObatMasuk

class InventoryObatListView(IsAuthenticated, ListView):
    model = InventoryObat
    template_name = 'inventory_obat/list.html'
    context_object_name = 'list_inventory_obat'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat'
        context['header_title'] = 'List Inventory Obat'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('inventory-obat-create')
        return context

class InventoryObatCreateView(IsAuthenticated, CreateView):
    model = InventoryObat
    template_name = 'component/form.html'
    form_class = InfentoryObatForm
    success_url = reverse_lazy('inventory-obat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat'
        context['header_title'] = 'Tambah Inventory Obat'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class InventoryObatUpdateView(IsAuthenticated, UpdateView):
    model = InventoryObat
    template_name = 'component/form.html'
    form_class = InfentoryObatForm
    success_url = reverse_lazy('inventory-obat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventor yObat'
        context['header_title'] = 'Edit Inventory Obat'
        return context

class InventoryObatDetailView(IsAuthenticated, DetailView):
    model = InventoryObat
    template_name = 'inventory_obat/detail.html'
    context_object_name = 'obat'

    def get_context_data(self, **kwargs):
        masuk = ObatMasuk.objects.aggregate(total=models.Sum('jumlah'))
        keluar = ObatKeluar.objects.aggregate(total=models.Sum('jumlah'))

        context = super().get_context_data(**kwargs)
        context['header'] = f'Obat {self.get_object().name}'
        context['header_title'] = f'Detail  Obat {self.get_object().name}'
        context['obat_masuk'] = masuk['total'] or 0
        context['obat_keluar'] = keluar['total'] or 0
        return context

class InventoryObatDeleteView(IsAuthenticated, DeleteView):
    model = InventoryObat
    template_name = 'component/delete.html'
    success_url = reverse_lazy('inventory-obat-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat'
        context['header_title'] = 'Delete Inventory Obat'
        return context
