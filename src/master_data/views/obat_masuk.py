# myapp/views.py

from operator import ge
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from master_data.form.inventory_obat_form import ObatMasukForm
from master_data.models import InventoryObat, ObatMasuk

class ObatMasukListView(IsAuthenticated, ListView):
    model = ObatMasuk
    template_name = 'inventory_obat_masuk/list.html'
    context_object_name = 'obat_masuk'
    

    def get_obat(self):
        return InventoryObat.objects.get(id=self.kwargs['inv_obat_id'])
    
    def get_queryset(self):
        if self.kwargs.get('inv_obat_id'):
            return self.model.objects.filter(obat__id=self.kwargs['inv_obat_id'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = f'Obat Masuk {self.get_obat().name}'
        context['header_title'] = f'List Obat Masuk {self.get_obat().name}'
        context['obat'] = self.get_obat()
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('obat-masuk-create', kwargs={'inv_obat_id': self.kwargs['inv_obat_id']})
        return context

class ObatMasukCreateView(IsAuthenticated, CreateView):
    model = ObatMasuk
    template_name = 'component/form.html'
    form_class = ObatMasukForm

    def get_obat(self):
        return InventoryObat.objects.get(id=self.kwargs['inv_obat_id'])

    def get_success_url(self) -> str:
        return reverse_lazy('obat-masuk-list', kwargs={'inv_obat_id': self.kwargs['inv_obat_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = f'Obat Masuk {self.get_obat().name}'
        context['header_title'] = f'Tambah  Obat Masuk {self.get_obat().name}'
        return context

    def form_valid(self, form):
        form.instance.obat = InventoryObat.objects.get(id=self.kwargs['inv_obat_id'])
        form.save()
        inv_obat = InventoryObat.objects.get(id=self.kwargs['inv_obat_id'])
        inv_obat.stok += form.instance.jumlah
        inv_obat.save()
        return super().form_valid(form)

class ObatMasukUpdateView(IsAuthenticated, UpdateView):
    model = ObatMasuk
    template_name = 'component/form.html'
    form_class = ObatMasukForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('obat-masuk-list', kwargs={'inv_obat_id': self.get_object().obat.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventor yObat'
        context['header_title'] = 'Edit Inventory Obat Masuk'
        return context

    def form_valid(self, form):
        form.instance.obat = self.get_object().obat
        form.save()
        return super().form_valid(form)

class ObatMasukDetailView(IsAuthenticated, DetailView):
    model = ObatMasuk
    template_name = 'inventory_obat/detail.html'
    context_object_name = 'detail_inventory_obat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat Masuk'
        context['header_title'] = 'Detail Inventory Obat Masuk'
        return context

class ObatMasukDeleteView(IsAuthenticated, DeleteView):
    model = ObatMasuk
    template_name = 'component/delete.html'
    success_url = reverse_lazy('obat-masuk-list')

    def get_success_url(self) -> str:
        return reverse_lazy('obat-masuk-list', kwargs={'inv_obat_id': self.get_object().obat.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Inventory Obat Masuk'
        context['header_title'] = 'Delete Inventory Obat Masuk'
        return context
