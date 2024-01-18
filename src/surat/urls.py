from django.urls import path, include
from surat.views.keterangan_sakit_views import *
from surat.views.keterangan_sehat_views import *
from surat.views.perintah_tugas import DownloadSuratPerintahTugas, SuratPerintahTugasCreateView, SuratPerintahTugasDeleteView, SuratPerintahTugasListView, SuratPerintahTugasUpdateView
from surat.views.rapid_views import *
from surat.views.rujukan_views import *
from surat.views.kelahiran_views import *
from surat.views.kematian_views import *

urlpatterns = [
    path("surat/", include([
        path("keterangan-sakit/", include([
            path('', KeteraganSakitListView.as_view(), name='keterangan-sakit-list'),
            path('create/', KeteraganSakitCreateView.as_view(), name='keterangan-sakit-create'),
            path('update/<uuid:pk>/', KeteraganSakitUpdateView.as_view(), name='keterangan-sakit-update'),
            path('delete/<uuid:pk>/', KeteraganSakitDeleteView.as_view(), name='keterangan-sakit-delete'),
            path('download/<uuid:pk>/', DownloadKeteranganSakit.as_view(), name='keterangan-sakit-download'),
        ])),

        path("keterangan-sehat/", include([
            path('', KeteranganSehatListView.as_view(), name='keterangan-sehat-list'),
            path('create/', KeteranganSehatCreateView.as_view(), name='keterangan-sehat-create'),
            path('update/<uuid:pk>/', KeteranganSehatUpdateView.as_view(), name='keterangan-sehat-update'),
            path('delete/<uuid:pk>/', KeteranganSehatUpdateView.as_view(), name='keterangan-sehat-delete'),
            path('download/<uuid:pk>/', DownloadKeteranganSehat.as_view(), name='keterangan-sehat-download'),
        ])),

        path("surat-rujukan/", include([
            path('', SuratRujukanListView.as_view(), name='rujukan-list'),
            path('create/', SuratRujukanCreateView.as_view(), name='rujukan-create'),
            path('update/<uuid:pk>/', SuratRujukanUpdateView.as_view(), name='rujukan-update'),
            path('delete/<uuid:pk>/', SuratRujukanDeleteView.as_view(), name='rujukan-delete'),
            path('download/<uuid:pk>/', DownloadSuratRujukan.as_view(), name='rujukan-download'),
        ])),

        path("surat-kelahiran/", include([
            path('', SuratKelahiranListView.as_view(), name='kelahiran-list'),
            path('create/', SuratKelahiranCreateView.as_view(), name='kelahiran-create'),
            path('update/<uuid:pk>/', SuratKelahiranUpdateView.as_view(), name='kelahiran-update'),
            path('delete/<uuid:pk>/', SuratKelahiranDeleteView.as_view(), name='kelahiran-delete'),
            path('download/<uuid:pk>/', DownloadSuratKelahiran.as_view(), name='kelahiran-download'),
        ])),

        path("surat-kemation/", include([
            path('', SuratKematianListView.as_view(), name='kematian-list'),
            path('create/', SuratKematianCreateView.as_view(), name='kematian-create'),
            path('update/<uuid:pk>/', SuratKematianUpdateView.as_view(), name='kematian-update'),
            path('delete/<uuid:pk>/', SuratKematianDeleteView.as_view(), name='kematian-delete'),
            path('download/<uuid:pk>/', DownloadSuratKematian.as_view(), name='kematian-download'),
        ])),

        path("surat-rapid/", include([
            path('', SuratRapidAntigenListView.as_view(), name='rapid-list'),
            path('create/', SuratRapidAntigenCreateView.as_view(), name='rapid-create'),
            path('update/<uuid:pk>/', SuratRapidAntigenCreateView.as_view(), name='rapid-update'),
            path('delete/<uuid:pk>/', SuratRapidAntigenDeleteView.as_view(), name='rapid-delete'),
            path('download/<uuid:pk>/', DownloadSuratRapidAntigen.as_view(), name='rapid-download'),
        ])),

        path("surat-tugas/", include([
            path('', SuratPerintahTugasListView.as_view(), name='tugas-list'),
            path('create/', SuratPerintahTugasCreateView.as_view(), name='tugas-create'),
            path('update/<uuid:pk>/', SuratPerintahTugasUpdateView.as_view(), name='tugas-update'),
            path('delete/<uuid:pk>/', SuratPerintahTugasDeleteView.as_view(), name='tugas-delete'),
            path('download/<uuid:pk>/', DownloadSuratPerintahTugas.as_view(), name='tugas-download'),
        ])),
    ]))
]