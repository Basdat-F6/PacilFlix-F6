"""
URL configuration for pacilflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('daftar_favorit/', include('daftar_favorit.urls')),
    path('daftar_unduhan/', include('daftar_unduhan.urls')),
    path('trailers/', include('trailer.urls')),
    path('watch/', include('tayangan.urls')),
    path('reviews/', include('ulasan.urls', namespace='ulasan')),
    path('daftar_kontributor/', include('daftar_kontributor.urls')),
    path('langganan/', include('langganan.urls')),
]
