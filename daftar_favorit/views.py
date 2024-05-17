from django.shortcuts import render

# Create your views here.
def kelola_daftar_favorit(request):
    return render(request, 'daftar_favorit.html')