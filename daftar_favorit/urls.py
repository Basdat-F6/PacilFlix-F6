from django.urls import path
from . import views

app_name = "daftar_favorit"

urlpatterns = [
    path('kelola-daftar-favorit', views.kelola_daftar_favorit, name='kelola_daftar_favorit'),
]
