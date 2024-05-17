from django.urls import path
from daftar_kontributor.views import show_daftar_kontributor, show_daftar_kontributor_pemain, show_daftar_kontributor_penulis_skenario, show_daftar_kontributor_sutradara

app_name = 'daftar_kontributor'

urlpatterns = [
    path('', show_daftar_kontributor, name='show_daftar_kontributor'),
    path('pemain', show_daftar_kontributor_pemain, name='show_daftar_kontributor_pemain'),
    path('penulis_skenario', show_daftar_kontributor_penulis_skenario, name='show_daftar_kontributor_penulis_skenario'),
    path('sutradara', show_daftar_kontributor_sutradara, name='show_daftar_kontributor_sutradara'),
]