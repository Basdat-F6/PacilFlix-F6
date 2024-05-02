from django.shortcuts import render, redirect


def show_trailers(request):
    data = []
    context = {
        "data": data,
    }
    return render(request, "trailer_list.html", context)