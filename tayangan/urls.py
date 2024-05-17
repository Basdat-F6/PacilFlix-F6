from django.urls import path
from . import views

app_name = 'tayangan'

urlpatterns = [
    path('', views.top_global, name='watch'),
    path('detail-film/<uuid:id>/', views.detail_film, name='detail-film'),
    path('detail-series/<uuid:id>/', views.detail_series, name='detail-series'),
    path('search/', views.search, name='search'),
    path('top-indonesia/', views.top_indonesia, name='top-indonesia'),
    path('top-global/', views.top_global, name='top-global'),
    path('watch-film/<uuid:id_film>/', views.watch_film, name='watch-film'),
    path('detail-episode/<uuid:id_series>/<str:sub_judul>/', views.detail_episode, name='detail-episode'),
    path('watch-episode/<uuid:id_series>/<str:sub_judul>/', views.watch_episode, name='watch-episode'),

]
