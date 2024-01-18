# myapp/urls.py
from django.urls import path, include
from master_data.views.inventory_obat_views import *
from master_data.views.layanan_views import *
from master_data.views.obat_keluar import *
from master_data.views.poliklinik_views import *
from master_data.views.tenaga_medis_view import *
from master_data.views.jadwal_praktik import *
from master_data.views.obat_masuk import *

urlpatterns = [
    path("layanan/", include([
        path('', LayananListView.as_view(), name='layanan-list'),
        path('create/', LayananCreateView.as_view(), name='layanan-create'),
        path('update/<uuid:pk>/', LayananUpdateView.as_view(), name='layanan-update'),
        path('delete/<uuid:pk>/', LayananDeleteView.as_view(), name='layanan-delete'),
    ])),
    path("poli/", include([
        path('', PoliKlinikListView.as_view(), name='poliklinik-list'),
        path('create/', PoliKlinikCreateView.as_view(), name='poliklinik-create'),
        path('update/<uuid:pk>/', PoliKlinikUpdateView.as_view(), name='poliklinik-update'),
        path('delete/<uuid:pk>/', PoliKlinikDeleteView.as_view(), name='poliklinik-delete'),
    ])),

    path("tenage-medis/", include([
        path('', TenagaMedisListView.as_view(), name='tenaga_medis-list'),
        path('create/', TenagaMedisCreateView.as_view(), name='tenaga_medis-create'),
        path('update/<uuid:pk>/', TenagaMedisUpdateView.as_view(), name='tenaga_medis-update'),
        path('delete/<uuid:pk>/', TenagaMedisDeleteView.as_view(), name='tenaga_medis-delete'),
    ])),

    path("jadwal-tenaga-medis/", include([
        path('', JadwalTenagaMedisListView.as_view(), name='jadwal-list'),
        path('create/', JadwalTenagaMedisCreateView.as_view(), name='jadwal-create'),
        path('update/<uuid:pk>/', JadwalTenagaMedisUpdateView.as_view(), name='jadwal-update'),
        path('detail/<uuid:pk>/', JadwalTenagaMedisDetailView.as_view(), name='jadwal-detail'),
        path('delete/<uuid:pk>/', JadwalTenagaMedisDeleteView.as_view(), name='jadwal-delete'),
    ])),

    path("inventory-obat/", include([
        path('', InventoryObatListView.as_view(), name='inventory-obat-list'),
        path('create/', InventoryObatCreateView.as_view(), name='inventory-obat-create'),
        path('update/<uuid:pk>/', InventoryObatUpdateView.as_view(), name='inventory-obat-update'),
        path('detail/<uuid:pk>/', InventoryObatDetailView.as_view(), name='inventory-obat-detail'),
        path('delete/<uuid:pk>/', InventoryObatDeleteView.as_view(), name='inventory-obat-delete'),
    ])),

    path("inventory-obat-masuk/", include([
        path('<uuid:inv_obat_id>/', ObatMasukListView.as_view(), name='obat-masuk-list'),
        path('create/<uuid:inv_obat_id>/', ObatMasukCreateView.as_view(), name='obat-masuk-create'),
        path('update/<uuid:pk>/', ObatMasukUpdateView.as_view(), name='obat-masuk-update'),
        path('delete/<uuid:pk>/', ObatMasukDeleteView.as_view(), name='obat-masuk-delete'),
    ])),

    path("inventory-obat-keluar/", include([
        path('<uuid:inv_obat_id>/', ObatKeluarListView.as_view(), name='obat-keluar-list'),
        path('create/<uuid:inv_obat_id>/', ObatKeluarCreateView.as_view(), name='obat-keluar-create'),
        path('update/<uuid:pk>/', ObatKeluarUpdateView.as_view(), name='obat-keluar-update'),
        path('delete/<uuid:pk>/', ObatKeluarDeleteView.as_view(), name='obat-keluar-delete'),
    ])),

    path('jadwal/', JadwalView.as_view(), name='jadwal-view'),
]
