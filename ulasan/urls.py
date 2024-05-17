from django.urls import path
from . import views

app_name = 'ulasan'

urlpatterns = [
    path('', views.review_page, name= 'show-reviews'),
    path('detail-review/<uuid:id_tayangan>', views.show_reviews, name='show-review'),
    path('add-review/<uuid:id_tayangan>/', views.add_review, name='add-review'),

]
