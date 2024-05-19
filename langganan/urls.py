from django.urls import path
from langganan.views import show_langganan, show_beli, bayar

app_name = 'langganan'

urlpatterns = [
    path('', show_langganan, name='show_langganan'),
    path('beli/<str:param_value>', show_beli, name='show_beli'),
    path('bayar/<str:metode>/<str:paket>', bayar, name='bayar'),
]