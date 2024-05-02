from django.shortcuts import render

# Create your views here.

def show_daftar_kontributor(request):
    return render(request, "daftar-kontributor.html")