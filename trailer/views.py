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

def query(query_str: str):
    result = []
    with connection.cursor() as cursor:
        try:
            cursor.execute(query_str)
            if query_str.strip().lower().startswith("select"):
                # Return hasil SELECT
                result = map_cursor(cursor)
            else:
                # Return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE (int)
                result = cursor.rowcount
        except Exception as e:
            # Return exception message
            result = str(e)
    return result

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

    # Ambil data film
    film = query(
        """
        SELECT T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, F.release_date_film as tanggal_rilis
        FROM "TAYANGAN" T
        JOIN "FILM" F ON T.id = F.id_tayangan
        ORDER BY T.judul
        """
    )

    # Ambil data series
    series = query(
        """
        SELECT T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, S.release_date as tanggal_rilis
        FROM "TAYANGAN" T
        JOIN "EPISODE" S ON T.id = S.id_series
        ORDER BY T.judul
        """
    )

    context = {
        "trailers": trailers if isinstance(trailers, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": trailers if not isinstance(trailers, list) else None,
    }

    return render(request, "trailer_list.html", context)

def show_top_indo(request):
    set_search_path()  # Set search_path ke skema 'pacilflix'

    # Ambil data top 10 tayangan berdasarkan jumlah viewer selama 7 hari terakhir
    top_indonesia = query(
        """
        SELECT T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, T.release_date_trailer as tanggal_rilis,
               COUNT(R.id_tayangan) as total_view
        FROM "TAYANGAN" T
        JOIN "RIWAYAT_NONTON" R ON T.id = R.id_tayangan
        WHERE R.durasi_tonton >= 0.7 * (
            SELECT CASE
                WHEN F.durasi_film IS NOT NULL THEN F.durasi_film
                ELSE S.durasi
            END
            FROM "TAYANGAN" T
            LEFT JOIN "FILM" F ON T.id = F.id_tayangan
            LEFT JOIN "EPISODE" S ON T.id = S.id_series
            WHERE T.id = R.id_tayangan
        )
        AND R.waktu_nonton >= NOW() - INTERVAL '7 days'
        GROUP BY T.id
        ORDER BY total_view DESC
        LIMIT 10
        """
    )

    context = {
        "trailers": top_indonesia if isinstance(top_indonesia, list) else [],
        "error": top_indonesia if not isinstance(top_indonesia, list) else None,
    }
    print(context)
    return render(request, "trailer_list.html", context)

def show_top_global(request):
    set_search_path()  # Set search_path ke skema 'pacilflix'

    # Ambil 10 trailer terbaik secara global
    top_global = query(
        """
        SELECT T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, T.release_date_trailer as tanggal_rilis
        FROM "TAYANGAN" T
        ORDER BY T.judul
        LIMIT 10
        """
    )

    # Ambil data film
    film = query(
        """
        SELECT T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, F.release_date_film as tanggal_rilis
        FROM "TAYANGAN" T
        JOIN "FILM" F ON T.id = F.id_tayangan
        ORDER BY T.judul
        LIMIT 10
        """
    )

    # Ambil data series
    series = query(
        """
        SELECT T.judul, T.sinopsis_trailer as sinopsis, T.url_video_trailer as trailer_url, S.release_date as tanggal_rilis
        FROM "TAYANGAN" T
        JOIN "EPISODE" S ON T.id = S.id_series
        ORDER BY T.judul
        LIMIT 10
        """
    )

    context = {
        "trailers": top_global if isinstance(top_global, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": top_global if not isinstance(top_global, list) else None,
    }

    return render(request, "trailer_list.html", context)
