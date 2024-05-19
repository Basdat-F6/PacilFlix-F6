from django.urls import path
from . import views

app_name = "daftar_favorit"

urlpatterns = [
    path('kelola-daftar-favorit', views.kelola_daftar_favorit, name='kelola_daftar_favorit'),
    path('detail/<str:judul>/', views.detail_daftar, name='detail_daftar'),
    path('delete-daftar', views.delete_daftar, name='delete_daftar'),
    path('delete-tayangan', views.delete_tayangan, name='delete_tayangan'),
    path('add', views.add, name="add")
]
