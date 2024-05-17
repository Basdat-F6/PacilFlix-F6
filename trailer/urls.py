from django.urls import path
from .views import *
app_name = 'trailer'

urlpatterns = [
    path('', show_top_global, name= 'show-trailers'),
    path('top-indonesia/', show_top_indo, name= 'top-indonesia'),
    path('top-global/', show_top_global, name= 'top-global'),
    path('search/', search, name= 'search'),
]