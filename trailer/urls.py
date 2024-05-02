from django.urls import path
from .views import *
app_name = 'trailer'

urlpatterns = [
    path('', show_trailers, name= 'show-trailers'),
]