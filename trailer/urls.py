from django.urls import path
from .views import *
app_name = 'trailer'

urlpatterns = [
    path('', show_trailers, name= 'show-trailers'),
    path('top-indonesia/', show_top_indo, name= 'top-indonesia'),
]