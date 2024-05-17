from django.urls import path
from . import views

app_name = 'tayangan'

urlpatterns = [
    path('', views.watch, name='watch'),
    path('detail-film/<uuid:id>/', views.detail_film, name='detail-film'),
    path('detail-series/<uuid:id>/', views.detail_series, name='detail-series'),
    path('episode/<uuid:id>/', views.episode, name='episode'),
    path('search/', views.search, name='search'),
    path('top-indonesia/', views.top_indonesia, name='top-indonesia'),
    path('top-global/', views.top_global, name='top-global'),
]
