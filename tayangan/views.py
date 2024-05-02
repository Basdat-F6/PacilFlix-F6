from django.shortcuts import render, redirect


def watch(request):
    data = []
    context = {
        "data": data,
    }
    return render(request, "tayangan.html", context)


def detail_film(request):
    data = []
    context = {
        "data": data,
    }
    return render(request, "detail_film.html", context)

def detail_series(request):
    data = []
    context = {
        "data": data,
    }
    return render(request, "detail_series.html", context)

def episode(request):
    data = []
    context = {
        "data": data,
    }
    return render(request, "episode.html", context)

def search(request):
    data = []
    context = {
        "data": data,
    }
    return render(request, "hasil_pencarian.html", context)