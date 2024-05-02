from django.urls import path
from .views import *
app_name = 'tayangan'

urlpatterns = [
    path('', watch, name= 'watch'),
    path('detail-film/', detail_film, name='detail-film'),
    path('detail-series/', detail_series, name='detail-series'),
    path('episode/', episode, name='episode'),
    path('search/', search, name='search'),

]