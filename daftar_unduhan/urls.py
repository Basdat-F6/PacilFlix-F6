from django.urls import path
from . import views

app_name = "daftar_unduhan"

urlpatterns = [
    path('kelola-daftar-unduhan', views.kelola_daftar_unduhan, name='kelola_daftar_unduhan'),
]
