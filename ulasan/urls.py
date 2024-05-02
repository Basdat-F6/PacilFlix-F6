from django.urls import path
from .views import *
app_name = 'ulasan'

urlpatterns = [
    path('', review_page, name= 'show-reviews'),
]