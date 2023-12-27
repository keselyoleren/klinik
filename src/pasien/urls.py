# myapp/urls.py
from django.urls import path, include
from pasien.views.pasien_views import *
from pasien.views.rawat_jalan_views import *
from pasien.views.rekam_medis_views import ListRawatJalanView

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
        path('delete/<uuid:pk>/', RawatJalanDeleteView.as_view(), name='rawat_jalan-delete'),
    ])),

    path("rekam-medis/", include([
        path('list-pasien', ListRawatJalanView.as_view(), name='rekam_medis-list-pasien'),
    ])),
]
