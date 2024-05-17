from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.contrib import messages  

def set_search_path():
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO 'pacilflix'")

def map_cursor(cursor):
    description = cursor.description
    query_result = namedtuple("Data", [col[0] for col in description])
    return [query_result(*row) for row in cursor.fetchall()]

def query(query_str: str, params=None):
    result = []
    with connection.cursor() as cursor:
        try:
            if params:
                cursor.execute(query_str, params)
            else:
                cursor.execute(query_str)
            if query_str.strip().lower().startswith("select"):
                result = map_cursor(cursor)
            else:
                result = cursor.rowcount
        except Exception as e:
            result = str(e)
    return result

def show_reviews(request, id_tayangan):
    set_search_path()

    # Ambil detail tayangan
    tayangan = query(
        """
        SELECT id, judul
        FROM "TAYANGAN"
        WHERE id = %s
        """, [id_tayangan]
    )

    if not tayangan:
        return HttpResponse("Tayangan not found", status=404)

    # Ambil ulasan dari tayangan
    reviews = query(
        """
        SELECT username, rating, deskripsi
        FROM "ULASAN"
        WHERE id_tayangan = %s
        ORDER BY timestamp DESC
        """, [id_tayangan]
    )

    username_cookie = request.COOKIES.get('username')
    context = {
        'username_cookie': username_cookie,
        "tayangan": tayangan[0],
        "reviews": reviews if isinstance(reviews, list) else [],
        "error_message": reviews if not isinstance(reviews, list) else None,
    }
    print(context)

    return render(request, "ulasan.html", context)


def add_review(request, id_tayangan):
    set_search_path()
    username_cookie = request.COOKIES.get('username')
    if request.method == "POST":
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        timestamp = timezone.now()        
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                INSERT INTO "ULASAN" (id_tayangan, username, timestamp, rating, deskripsi)
                VALUES (%s, %s, %s, %s, %s)
                """, [id_tayangan, username_cookie, timestamp, rating, description])
                messages.success(request, "Review added successfully!")
                return redirect('ulasan:show-review', id_tayangan=id_tayangan)
            except Exception as e:
                messages.error(request, str(e))

    tayangan = query(
        """
        SELECT id, judul
        FROM "TAYANGAN"
        WHERE id = %s
        """, [id_tayangan]
    )

    if not tayangan:
        print('Tayangan tidak ditemukan')

    # Ambil ulasan dari tayangan
    reviews = query(
        """
        SELECT username, rating, deskripsi
        FROM "ULASAN"
        WHERE id_tayangan = %s
        ORDER BY timestamp DESC
        """, [id_tayangan]
    )

    context = {
        'username_cookie': username_cookie,
        "tayangan": tayangan[0],
        "reviews": reviews if isinstance(reviews, list) else [],
    }

    print('OKE TERKIRIM', context)

    return render(request, "ulasan.html", context)