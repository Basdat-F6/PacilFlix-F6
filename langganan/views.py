from django.shortcuts import render

def show_langganan(request):
    return render(request, "langganan.html")

def show_beli(request):
    return render(request, "beli.html")