# myapp/urls.py
from django.urls import path, include
from pasien.views.assesment_fisioterapi_views import *
from pasien.views.assesment_rawat_jalan_views import *
from pasien.views.assesment_rawatinap import *
from pasien.views.catatan_terintegrasi_views import *
from pasien.views.fisio_terapi_views import *
from pasien.views.informed_consent_views import *
from pasien.views.monitoring_views import *
from pasien.views.obat_views import * 
from pasien.views.pasien_views import *
from pasien.views.permintaan_labor2_view import *
from pasien.views.permintaan_labor_view import *
from pasien.views.rawat_inap_views import * 
from pasien.views.rawat_jalan_views import *
from pasien.views.rekam_medis_views import *
from pasien.views.rekam_medis_views import *
from pasien.views.resume_fisioterapi_views import *
from pasien.views.resume_views import *
from pasien.views.rincian_biaya_views import *
from pasien.views.rujukan_keluar_fisoterapi_views import *

urlpatterns = [
    path("pasien/", include([
        path('', PasienListView.as_view(), name='pasien-list'),
        path('create/', PasienCreateView.as_view(), name='pasien-create'),
        path('update/<uuid:pk>/', PasienUpdateView.as_view(), name='pasien-update'),
        path('delete/<uuid:pk>/', PasienDeleteView.as_view(), name='pasien-delete'),
        path('register/', include([
            path('rawat-jalan/<uuid:pasien_id>/', PasienRawatJalanRegisterViwe.as_view(), name='register-rawat-jalan'),
            path('rawat-inap/<uuid:pasien_id>/', PasienRawatInapRegisterView.as_view(), name='register-rawat-inap'),
            path('fisio-terapi/<uuid:pasien_id>/', PasienFisioTerapiRegisterView.as_view(), name='register-fisio-terapi'),
        ])),
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

        path("assesment/", include([
            path('create/<uuid:pasien_id>/', AssessmentRawatInapCreateView.as_view(), name='assesment-rawat-inap-create'),
            path('update/<uuid:pk>/', AssessmentRawatInapUpdateView.as_view(), name='assesment-rawat-inap-update'),
            path('delete/<uuid:pk>/', AssessmentRawatInapDeleteView.as_view(), name='assesment-rawat-inap-delete'),
            path('download/<uuid:pk>/', DownloadAssesmentRawatInapView.as_view(), name='assesment-rawat-inap-download'),
        ])),

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
        path('list/', BiayaListView.as_view(), name='biaya-list'),
        path('create/<uuid:pasien_rawat_inap_id>/', RincianBiayaCreateView.as_view(), name='rincian-biaya-create'),
        path('update/<uuid:pk>/', RincianBiayaUpdateView.as_view(), name='rincian-biaya-update'),
        path('delete/<uuid:pk>/', RincianBiayaDeleteView.as_view(), name='rincian-biaya-delete'),
        path('export/<uuid:pasien_rawat_inap_id>/', DownloadRincianBiaya.as_view(), name='rincian-biaya-download'),
    ])),

    
    path("fisioterapi/", include([
        path('', PasienFisioterapiListView.as_view(), name='fisio_terapi-list'),
        path('create/', PasienFisioterapiCreateView.as_view(), name='fisio_terapi-create'),
        path('update/<uuid:pk>/', PasienFisioterapiUpdateView.as_view(), name='fisio_terapi-update'),

        path("assesment/", include([
            path('create/<uuid:pasien_id>/', AssesMentFisioTerapiCreateView.as_view(), name='assesment-awal-fisioterapi-create'),
            path('update/<uuid:pk>/', AssesMentFisioTerapiUpdateView.as_view(), name='assesment-fisioterapi-update'),
            path('delete/<uuid:pk>/', AssesMentFisioTerapiDeleteView.as_view(), name='assesment-fisioterapi-delete'),
            path('download/<uuid:pk>/', DownloadAssesmentAwalVisioterapiView.as_view(), name='assesment-fisioterapi-download'),
        ])),

        path("informed/", include([
            path('create/<uuid:pasien_id>/', InformedConsentCreateView.as_view(), name='informed-create'),
            path('update/<uuid:pk>/', InformedConsentUpdateView.as_view(), name='informed-update'),
            path('delete/<uuid:pk>/', InformedConsentDeleteView.as_view(), name='informed-delete'),
            path('download/<uuid:pk>/', DownloadInvormedApiView.as_view(), name='informed-download'),
        ])),

        path("rujukan-keluar/", include([
            path('create/<uuid:pasien_id>/', RujukanKeluarCreateView.as_view(), name='rujukan_keluar-create'),
            path('update/<uuid:pk>/', RujukanKeluarUpdateView.as_view(), name='rujukan_keluar-update'),
            path('delete/<uuid:pk>/', RujukanKeluarDeleteView.as_view(), name='rujukan_keluar-delete'),
            path('download/<uuid:pk>/', DownloadRujukanKeluarVisioterapiView.as_view(), name='rujukan_keluar-download'),
        ])),

        path("resume/", include([
            path('create/<uuid:pasien_id>/', ResumeFisioterapiCreateView.as_view(), name='resume_fisioterapi-create'),
            path('update/<uuid:pk>/', ResumeFisioterapiUpdateView.as_view(), name='resume_fisioterapi-update'),
            path('delete/<uuid:pk>/', ResumeFisioterapiDeleteView.as_view(), name='resume_fisioterapi-delete'),
            path('download/<uuid:pk>/', DownloadResumetVisioterapiView.as_view(), name='resume_fisioterapi-download'),
        ])),

        path("monitoring/", include([
            path('<uuid:pasien_id>/', MonitoringFisoterapiListView.as_view(), name='monitor-fisioterapi-list'),
            path('create/<uuid:pasien_id>/', MonitoringFisoterapiCreateView.as_view(), name='monitor-fisioterapi-create'),
            path('update/<uuid:pk>/', MonitoringFisoterapiUpdateView.as_view(), name='monitor-fisioterapi-update'),
            path('delete/<uuid:pk>/', MonitoringFisoterapiDeleteView.as_view(), name='monitor-fisioterapi-delete'),
            path('export/<uuid:pasien_id>/', DownloadMonitoringFisoterapi.as_view(), name='monitor-fisioterapi-download'),
        ])),

        
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

    path("laboratorium/", include([
        path("permintaan/", include([
            path('<uuid:pasien_id>/', PermintaanLaborListView.as_view(), name='permintaan-labor-list'),
            path('create/<uuid:pasien_id>/', PermintaanLaborCreateView.as_view(), name='permintaan-labor-create'),
            path('update/<uuid:pk>/', PermintaanLaborUpdateView.as_view(), name='permintaan-labor-update'),
            path('delete/<uuid:pk>/', PermintaanLaborDeleteView.as_view(), name='permintaan-labor-delete'),
            path('export/<uuid:pk>/', DownloadPermintaanLabor.as_view(), name='permintaan-labor-download'),
        ])),
        path("permintaan2/", include([
            path('<uuid:pasien_id>/', PermintaanLabor2ListView.as_view(), name='permintaan-labor2-list'),
            path('create/<uuid:pasien_id>/', PermintaanLabor2CreateView.as_view(), name='permintaan-labor2-create'),
            path('update/<uuid:pk>/', PermintaanLabor2UpdateView.as_view(), name='permintaan-labor2-update'),
            path('delete/<uuid:pk>/', PermintaanLabor2DeleteView.as_view(), name='permintaan-labor2-delete'),
            path('export/<uuid:pk>/', DownloadPermintaanLabor2.as_view(), name='permintaan-labor2-download'),
        ]))
    ])),
]

