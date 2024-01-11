# myapp/urls.py
from django.urls import path, include
from pasien.models import RekamMedis
from pasien.views.assesment_rawat_jalan_views import *
from pasien.views.catatan_terintegrasi_views import *
from pasien.views.pasien_views import *
from pasien.views.rawat_jalan_views import *
from pasien.views.rekam_medis_views import *
from pasien.views.rekam_medis_views import *

urlpatterns = [
    path("pasien/", include([
        path('', PasienListView.as_view(), name='pasien-list'),
        path('create/', PasienCreateView.as_view(), name='pasien-create'),
        path('update/<uuid:pk>/', PasienUpdateView.as_view(), name='pasien-update'),
        path('delete/<uuid:pk>/', PasienDeleteView.as_view(), name='pasien-delete'),
    ])),

    path("rawat-jalan/", include([
        path('', RawatJalanListView.as_view(), name='rawat_jalan-list'),
        path('create/', RawatJalanCreateView.as_view(), name='rawat_jalan-create'),
        path('update/<uuid:pk>/', RawatJalanUpdateView.as_view(), name='rawat_jalan-update'),
        path('assesment/create/<uuid:pasien_id>/', AssesmentRawatJalanCreateView.as_view(), name='assesment-awal-rawat-jalan-create'),
        path('assesment/update/<uuid:pk>/', AssesmentRawatJalanUpdateView.as_view(), name='assesment-rawat-jalan-update'),
        path('assesment/delete/<uuid:pk>/', AssesmentRawatJalanDeleteView.as_view(), name='assesment-awal-rawat-jalan-delete'),
        path('assesment/download/<uuid:pk>/', DownloadAssesmentView.as_view(), name='assesment-awal-rawat-jalan-download'),
        path('delete/<uuid:pk>/', RawatJalanDeleteView.as_view(), name='rawat_jalan-delete'),
        
        
        path('catatan-terintegrasi/<uuid:pasien_rawat_jalan_id>/', CatanTerintegrasiListView.as_view(), name='catatan-terintegrasi-list'),
        path('catatan-terintegrasi/create/<uuid:pasien_rawat_jalan_id>/', CatanTerintegrasiCreateView.as_view(), name='catatan-terintegrasi-create'),
        path('catatan-terintegrasi/update/<uuid:pk>/', CatanTerintegrasiUpdateView.as_view(), name='catatan-terintegrasi-update'),
        path('catatan-terintegrasi/delete/<uuid:pk>/', CatanTerintegrasiDeleteView.as_view(), name='catatan-terintegrasi-delete'),
        path('catatan-terintegrasi/export/<uuid:pasien_rawat_jalan_id>/', DownloadCatatanTerIntegrasi.as_view(), name='catatan-terintegrasi-download'),

    ])),

    path("rekam-medis/", include([
        path('', RekamMedisListView.as_view(), name='rekam_medis-list'),
        path('create/<uuid:pasien_id>/', RekamMedisCreateView.as_view(), name='rekam_medis-create'),
        path('riwayat/<uuid:pasien_id>/', RiwayatRekamMedisListView.as_view(), name='riwayat_rekam_medis'),
        path('update/<uuid:pk>/', RekamMedisUpdateView.as_view(), name='rekam_medis-update'),
        path('delete/<uuid:pk>/', RekamMedisDeleteView.as_view(), name='rekam_medis-delete'),
        path('download/<uuid:pk>/', DownloadRekamMedisView.as_view(), name='rekam_medis-download'),
        path('list-pasien', ListRawatJalanView.as_view(), name='rekam_medis-list-pasien'),
    ])),
]
