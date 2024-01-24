# myapp/urls.py
from django.urls import path, include
from pasien.models import RekamMedis
from pasien.views.assesment_rawat_jalan_views import *
from pasien.views.catatan_terintegrasi_views import *
from pasien.views.fisio_terapi_views import *
from pasien.views.obat_views import * 
from pasien.views.pasien_views import *
from pasien.views.rawat_inap_views import * 
from pasien.views.rawat_jalan_views import *
from pasien.views.rekam_medis_views import *
from pasien.views.rekam_medis_views import *
from pasien.views.resume_views import DownloadResume, ResumeCreateView, ResumeDeleteView, ResumeListView, ResumeUpdateView
from pasien.views.rincian_biaya_views import DownloadRincianBiaya, RincianBiayaCreateView, RincianBiayaDeleteView, RincianBiayaListView, RincianBiayaUpdateView

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
              
    ])),

    path("catatan-terintegrasi/", include([
        path('<uuid:pasien_rawat_jalan_id>/', CatanTerintegrasiListView.as_view(), name='catatan-terintegrasi-list'),
        path('create/<uuid:pasien_rawat_jalan_id>/', CatanTerintegrasiCreateView.as_view(), name='catatan-terintegrasi-create'),
        path('update/<uuid:pk>/', CatanTerintegrasiUpdateView.as_view(), name='catatan-terintegrasi-update'),
        path('delete/<uuid:pk>/', CatanTerintegrasiDeleteView.as_view(), name='catatan-terintegrasi-delete'),
        path('export/<uuid:pasien_rawat_jalan_id>/', DownloadCatatanTerIntegrasi.as_view(), name='catatan-terintegrasi-download'),
    ])),  

    path("rawat-inap/", include([
        path('', RawatInapListView.as_view(), name='rawat_inap-list'),
        path('create/', RawatInapCreateView.as_view(), name='rawat_inap-create'),
        path('update/<uuid:pk>/', RawatInapUpdateView.as_view(), name='rawat_inap-update'),
        path('delete/<uuid:pk>/', RawatInapDeleteView.as_view(), name='rawat_inap-delete'),
    ])),

    path("obat/", include([
        path('<uuid:pasien_rawat_inap_id>/', ObatListView.as_view(), name='obat-list'),
        path('create/<uuid:pasien_rawat_inap_id>/', ObatCreateView.as_view(), name='obat-create'),
        path('update/<uuid:pk>/', ObatUpdateView.as_view(), name='obat-update'),
        path('delete/<uuid:pk>/', ObatDeleteView.as_view(), name='obat-delete'),
        path('export/<uuid:pasien_rawat_inap_id>/', DownloadObat.as_view(), name='obat-download'),
    ])),

    path("resume/", include([
        path('<uuid:pasien_id>/', ResumeListView.as_view(), name='resume-list'),
        path('create/<uuid:pasien_id>/', ResumeCreateView.as_view(), name='resume-create'),
        path('update/<uuid:pk>/', ResumeUpdateView.as_view(), name='resume-update'),
        path('delete/<uuid:pk>/', ResumeDeleteView.as_view(), name='resume-delete'),
        path('export/<uuid:pasien_id>/', DownloadResume.as_view(), name='resume-download'),
    ])),


    path("rincian-biaya/", include([
        path('<uuid:pasien_rawat_inap_id>/', RincianBiayaListView.as_view(), name='rincian-biaya-list'),
        path('create/<uuid:pasien_rawat_inap_id>/', RincianBiayaCreateView.as_view(), name='rincian-biaya-create'),
        path('update/<uuid:pk>/', RincianBiayaUpdateView.as_view(), name='rincian-biaya-update'),
        path('delete/<uuid:pk>/', RincianBiayaDeleteView.as_view(), name='rincian-biaya-delete'),
        path('export/<uuid:pasien_rawat_inap_id>/', DownloadRincianBiaya.as_view(), name='rincian-biaya-download'),
    ])),

    
    path("fisioterapi/", include([
        path('', PasienFisioterapiListView.as_view(), name='fisio_terapi-list'),
        path('create/', PasienFisioterapiCreateView.as_view(), name='fisio_terapi-create'),
        path('update/<uuid:pk>/', PasienFisioterapiUpdateView.as_view(), name='fisio_terapi-update'),
        path('delete/<uuid:pk>/', PasienFisioterapiDeleteView.as_view(), name='fisio_terapi-delete'),
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
