from django.shortcuts import render
from django.db import connection
from collections import namedtuple


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

str_film = """
    SELECT DISTINCT ON (T.judul) T.id, T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, T.release_date_trailer as tanggal_rilis, F.release_date_film
    FROM "TAYANGAN" T
    JOIN "FILM" F ON T.id = F.id_tayangan
    ORDER BY T.judul
    """


str_series = """
    SELECT DISTINCT ON (T.judul) T.id, T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, T.release_date_trailer as tanggal_rilis, S.release_date
    FROM "TAYANGAN" T
    JOIN "EPISODE" S ON T.id = S.id_series
    ORDER BY T.judul
    """


def show_trailers(request):
    set_search_path()  # Set search_path ke skema 'pacilflix'

    # Ambil semua trailer
    trailers = query(
        """
        SELECT T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, T.release_date_trailer as tanggal_rilis
        FROM "TAYANGAN" T
        ORDER BY T.judul
        LIMIT 10
        """
    )
    film = query(str_film)
    series = query(str_series)

    username_cookie = request.COOKIES.get('username')
    context = {
        "username_cookie": username_cookie,
        "trailers": trailers if isinstance(trailers, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": trailers if not isinstance(trailers, list) else None,
    }

    return render(request, "trailer_list.html", context)

def search(request):
    set_search_path()
    query_str = request.GET.get("q", "")
    results = query(
        """
        SELECT id, judul, sinopsis_trailer as sinopsis, url_video_trailer, release_date_trailer
        FROM "TAYANGAN"
        WHERE judul ILIKE %s
        """, [f"%{query_str}%"]
    )
    
    username_cookie = request.COOKIES.get('username')
    context = {
        "username_cookie": username_cookie,
        "results": results if isinstance(results, list) else [],
        "error": results if not isinstance(results, list) else None,
    }
    return render(request, "hasil_pencarian.html", context)


def show_top_indo(request):
    set_search_path()
    username_cookie = request.COOKIES.get('username')

    # Ambil 10 trailer terbaik di Indonesia selama 7 hari terakhir
    top_indonesia = query(
        """
        SELECT T.id, T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, T.release_date_trailer as tanggal_rilis,
               COUNT(R.id_tayangan) as total_view,
               CASE
                   WHEN EXISTS (SELECT 1 FROM "FILM" F WHERE F.id_tayangan = T.id) THEN 'film'
                   ELSE 'series'
               END as tayangan_type
        FROM "TAYANGAN" T
        JOIN "RIWAYAT_NONTON" R ON T.id = R.id_tayangan
        JOIN "PENGGUNA" P ON R.username = P.username
        WHERE P.negara_asal = 'Indonesia'
        AND (EXTRACT(EPOCH FROM (R.end_date_time - R.start_date_time)) / 60) >= 0.7 * (
            SELECT COALESCE(F.durasi_film, S.durasi)
            FROM "TAYANGAN" T2
            LEFT JOIN "FILM" F ON T2.id = F.id_tayangan
            LEFT JOIN "EPISODE" S ON T2.id = S.id_series
            WHERE T2.id = T.id
            LIMIT 1
        )
        AND R.end_date_time >= NOW() - INTERVAL '7 days'
        GROUP BY T.id
        ORDER BY total_view DESC
        LIMIT 10
        """
    )

    film = query(str_film)
    series = query(str_series)

    context = {
        "username_cookie": username_cookie,
        "trailers": top_indonesia if isinstance(top_indonesia, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": top_indonesia if not isinstance(top_indonesia, list) else None,
    }

    return render(request, "trailer_list.html", context)

def show_top_global(request):
    set_search_path()
    username_cookie = request.COOKIES.get('username')

    # Ambil 10 trailer terbaik global selama 7 hari terakhir
    top_global = query(
        """
        SELECT T.id, T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, T.release_date_trailer as tanggal_rilis,
               COUNT(R.id_tayangan) as total_view,
               CASE
                   WHEN EXISTS (SELECT 1 FROM "FILM" F WHERE F.id_tayangan = T.id) THEN 'film'
                   ELSE 'series'
               END as tayangan_type
        FROM "TAYANGAN" T
        JOIN "RIWAYAT_NONTON" R ON T.id = R.id_tayangan
        JOIN "PENGGUNA" P ON R.username = P.username
        WHERE (EXTRACT(EPOCH FROM (R.end_date_time - R.start_date_time)) / 60) >= 0.7 * (
            SELECT COALESCE(F.durasi_film, S.durasi)
            FROM "TAYANGAN" T2
            LEFT JOIN "FILM" F ON T2.id = F.id_tayangan
            LEFT JOIN "EPISODE" S ON T2.id = S.id_series
            WHERE T2.id = T.id
            LIMIT 1
        )
        AND R.end_date_time >= NOW() - INTERVAL '7 days'
        GROUP BY T.id
        ORDER BY total_view DESC
        LIMIT 10
        """
    )
    film = query(str_film)
    series = query(str_series)

    context = {
        "username_cookie": username_cookie,
        "trailers": top_global if isinstance(top_global, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": top_global if not isinstance(top_global, list) else None,
    }

    return render(request, "trailer_list.html", context)
