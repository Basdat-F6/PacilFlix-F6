from django.urls import path
from main.views import show_landing_page, register, login_user, logout_user, show_welcome_page

app_name = 'main'

urlpatterns = [
    path('', show_landing_page, name='show_landing_page'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('welcome/', show_welcome_page, name='show_welcome_page'),
]