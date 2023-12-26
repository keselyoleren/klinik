# myapp/urls.py
from django.urls import path, include
from master_data.views.layanan_views import *
from master_data.views.poliklinik_views import *
from master_data.views.tenaga_medis_view import *
from master_data.views.jadwal_praktik import *



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
        path('delete/<uuid:pk>/', JadwalTenagaMedisDeleteView.as_view(), name='jadwal-delete'),
    ])),

    path('jadwal/', JadwalView.as_view(), name='jadwal-view'),
]
