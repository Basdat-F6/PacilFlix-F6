from django.shortcuts import render

def show_langganan(request):
    username_cookie = request.COOKIES.get('username')
    context = {
        'username_cookie': username_cookie
    }
    return render(request, "langganan.html", context)

def show_beli(request):
    username_cookie = request.COOKIES.get('username')
    context = {
        'username_cookie': username_cookie
    }
    return render(request, "beli.html", context)