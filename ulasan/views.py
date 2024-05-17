import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db import connection
from django.contrib.auth.decorators import login_required
from collections import namedtuple

from django.shortcuts import render
from django.http import HttpResponse

# Data ulasan hardcoded
reviews = [
    {'username': 'user1', 'description': 'Great movie!', 'rating': 5},
    {'username': 'user2', 'description': 'Pretty good.', 'rating': 4},
    {'username': 'user3', 'description': 'Not bad, but could be better.', 'rating': 3},
]

def review_page(request):
    if request.method == 'POST':
        # Menambah ulasan baru
        username = 'user_example'  # Contoh username
        description = request.POST.get('description')
        rating = request.POST.get('rating')
        reviews.insert(0, {'username': username, 'description': description, 'rating': rating})
    
    return render(request, 'ulasan.html', {'reviews': reviews})

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

    context = {
        "tayangan": tayangan[0],
        "reviews": reviews if isinstance(reviews, list) else [],
        "error": reviews if not isinstance(reviews, list) else None,
    }
    print(context)

    return render(request, "ulasan.html", context)

@login_required
def add_review(request, id_tayangan):
    set_search_path()

    if request.method == "POST":
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        username = request.user.username
        timestamp = datetime.now()

        # Menambahkan ulasan baru
        query(
            """
            INSERT INTO "ULASAN" (id_tayangan, username, timestamp, rating, deskripsi)
            VALUES (%s, %s, %s, %s, %s)
            """, [id_tayangan, username, timestamp, rating, description]
        )

        print("berhasil")

        return redirect('add-review', id_tayangan=id_tayangan)

    # Ambil detail tayangan
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
        "tayangan": tayangan[0],
        "reviews": reviews if isinstance(reviews, list) else [],
        "error": reviews if not isinstance(reviews, list) else None,
    }

    print('OKE TERKIRIM', context)

    return render(request, "ulasan.html", context)