from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import RegisterForm
from utils.query import *

def show_landing_page(request):
    return render(request, "landing-page.html")

def show_welcome_page(request):
    username_cookie = request.COOKIES.get('username')
    context = {
        'username_cookie': username_cookie
    }
    return render(request, "welcome.html", context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara_asal = request.POST.get('negara_asal')

        # Check if all fileds are filled
        if username and password and negara_asal:
            try:
                cursor.execute(f'INSERT INTO "PENGGUNA" VALUES (\'{username}\', \'{password}\',\'{negara_asal}\')')
                connection.commit()
                return redirect('main:login_user')
            
            except Exception as error:
                connection.rollback()
                error_message = str(error).split('CONTEXT')[0]
                messages.error(request, error_message)
        else:
            messages.error(request, 'Semua field harus diisi')
    
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }

    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        cursor.execute('SELECT * FROM "PENGGUNA" WHERE "username" = %s AND "password" = %s', (username, password))
        user = cursor.fetchall()
        if len(user) == 0:
            error_message = "Username atau password salah"
            messages.error(request, error_message)
            return redirect('main:login_user')
        else:
            response = HttpResponseRedirect(reverse('tayangan:watch'))
            response.set_cookie('username', username)
            return response

    return render(request, 'login.html')

def logout_user(request):
    response = HttpResponseRedirect(reverse('main:show_landing_page'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response