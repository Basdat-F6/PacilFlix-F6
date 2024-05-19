from django.urls import path
from daftar_kontributor.views import show_daftar_kontributor

app_name = 'daftar_kontributor'

urlpatterns = [
    path('<str:filter>', show_daftar_kontributor, name='show_daftar_kontributor'),
]