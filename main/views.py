from django.shortcuts import render

def show_landing_page(request):
    return render(request, "landing-page.html")
