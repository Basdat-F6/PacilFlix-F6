from django.http import HttpResponse
from django.shortcuts import render, redirect
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
                # Return hasil SELECT
                result = map_cursor(cursor)
            else:
                # Return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE (int)
                result = cursor.rowcount
        except Exception as e:
            # Return exception message
            result = str(e)
    return result


def watch(request):
    set_search_path()

    # Ambil semua tayangan
    tayangan = query(
        """
        SELECT id, judul, sinopsis, url_video_trailer, release_date_trailer
        FROM "TAYANGAN"
        ORDER BY judul
        """
    )

    # Ambil data film
    film = query(
        """
        SELECT T.id, T.judul, T.sinopsis, T.url_video_trailer, T.release_date_trailer, F.release_date_film
        FROM "TAYANGAN" T
        JOIN "FILM" F ON T.id = F.id_tayangan
        ORDER BY T.judul
        """
    )

    # Ambil data series
    series = query(
        """
        SELECT T.id, T.judul, T.sinopsis, T.url_video_trailer, T.release_date_trailer, S.release_date
        FROM "TAYANGAN" T
        JOIN "EPISODE" S ON T.id = S.id_series
        ORDER BY T.judul
        """
    )

    context = {
        "tayangan": tayangan if isinstance(tayangan, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": tayangan if not isinstance(tayangan, list) else None,
    }
    print(context)
    return render(request, "tayangan.html", context)

def detail_film(request, id):
    set_search_path()
    
    # Query untuk mengambil detail tayangan
    detail = query(
        """
        SELECT T.id, T.judul, T.sinopsis, T.url_video_trailer, T.release_date_trailer, F.release_date_film, F.durasi_film,
               (SELECT COUNT(R.id_tayangan) FROM "RIWAYAT_NONTON" R WHERE R.id_tayangan = T.id) as total_view,
               (SELECT AVG(U.rating) FROM "ULASAN" U WHERE U.id_tayangan = T.id) as rating_rata_rata,
               (SELECT STRING_AGG(G.genre, ', ') FROM "GENRE_TAYANGAN" G WHERE G.id_tayangan = T.id) as genre,
               T.asal_negara,
               (SELECT STRING_AGG(C.nama, ', ') FROM "PEMAIN" P JOIN "CONTRIBUTORS" C ON P.id = C.id JOIN "MEMAINKAN_TAYANGAN" TP ON P.id = TP.id_pemain WHERE TP.id_tayangan = T.id) as pemain,
               (SELECT STRING_AGG(C.nama, ', ') FROM "PENULIS_SKENARIO" P JOIN "CONTRIBUTORS" C ON P.id = C.id JOIN "MENULIS_SKENARIO_TAYANGAN" TP ON P.id = TP.id_penulis_skenario WHERE TP.id_tayangan = T.id) as penulis,
               (SELECT C.nama FROM "SUTRADARA" S JOIN "CONTRIBUTORS" C ON S.id = C.id WHERE S.id = T.id_sutradara) as sutradara
        FROM "TAYANGAN" T
        JOIN "FILM" F ON T.id = F.id_tayangan
        WHERE T.id = %s
        """, [id]
    )

    if not detail:
        return HttpResponse("Detail not found", status=404)
    
    context = {
        "detail": detail[0],
        "error": None,
    }
    return render(request, "detail_film.html", context)




def detail_series(request, id):
    set_search_path()

    # Query untuk mengambil detail tayangan
    detail = query(
        """
        SELECT T.id, T.judul, T.sinopsis, T.url_video_trailer, T.release_date_trailer,
               (SELECT COUNT(R.id_tayangan) FROM "RIWAYAT_NONTON" R WHERE R.id_tayangan = T.id) as total_view,
               (SELECT AVG(U.rating) FROM "ULASAN" U WHERE U.id_tayangan = T.id) as rating_rata_rata,
               (SELECT STRING_AGG(G.genre, ', ') FROM "GENRE_TAYANGAN" G WHERE G.id_tayangan = T.id) as genre,
               T.asal_negara,
               (SELECT STRING_AGG(C.nama, ', ') FROM "PEMAIN" P JOIN "CONTRIBUTORS" C ON P.id = C.id JOIN "MEMAINKAN_TAYANGAN" TP ON P.id = TP.id_pemain WHERE TP.id_tayangan = T.id) as pemain,
               (SELECT STRING_AGG(C.nama, ', ') FROM "PENULIS_SKENARIO" P JOIN "CONTRIBUTORS" C ON P.id = C.id JOIN "MENULIS_SKENARIO_TAYANGAN" TP ON P.id = TP.id_penulis_skenario WHERE TP.id_tayangan = T.id) as penulis,
               (SELECT C.nama FROM "SUTRADARA" S JOIN "CONTRIBUTORS" C ON S.id = C.id WHERE S.id = T.id_sutradara) as sutradara
        FROM "TAYANGAN" T
        WHERE T.id = %s
        """, [id]
    )

    if not detail:
        return HttpResponse("Detail not found", status=404)

    # Query untuk mengambil data episode terkait series ini
    episodes = query(
        """
        SELECT E.id_series, E.sub_judul, E.sinopsis, E.durasi, E.url_video, E.release_date
        FROM "EPISODE" E
        WHERE E.id_series = %s
        ORDER BY E.release_date
        """, [id]
    )

    context = {
        "detail": detail[0],
        "episodes": episodes if isinstance(episodes, list) else [],
        "error": None,
    }
    return render(request, "detail_series.html", context)

def episode(request, id):
    set_search_path()
    
    # Ambil detail episode yang diminta
    episode_detail = query(
        """
        SELECT E.id_series, E.sub_judul, E.sinopsis, E.durasi, E.url_video, E.release_date
        FROM "EPISODE" E
        WHERE E.id_series = %s
        """, [id]
    )

    # Ambil semua episode dari series yang sama
    episodes = query(
        """
        SELECT E.id_series, E.sub_judul, E.sinopsis, E.durasi, E.url_video, E.release_date
        FROM "EPISODE" E
        WHERE E.id_series = %s
        ORDER BY E.release_date
        """, [id]
    )
    
    # Ambil detail tayangan series
    series_detail = query(
        """
        SELECT T.id, T.judul
        FROM "TAYANGAN" T
        JOIN "SERIES" S ON T.id = S.id_tayangan
        WHERE T.id = %s
        """, [id]
    )

    if not episode_detail:
        return HttpResponse("Episode not found", status=404)

    context = {
        "episode": episode_detail[0] if isinstance(episode_detail, list) and episode_detail else None,
        "episodes": episodes if isinstance(episodes, list) else [],
        "detail": series_detail[0] if isinstance(series_detail, list) and series_detail else None,
        "error": episodes if not isinstance(episodes, list) else None,
    }
    return render(request, "episode.html", context)


def search(request):
    set_search_path()
    query_str = request.GET.get("q", "")
    results = query(
        """
        SELECT id, judul, sinopsis, url_video_trailer, release_date_trailer
        FROM "TAYANGAN"
        WHERE judul ILIKE %s
        """, [f"%{query_str}%"]
    )
    context = {
        "results": results if isinstance(results, list) else [],
        "error": results if not isinstance(results, list) else None,
    }
    return render(request, "hasil.html", context)


def top_indonesia(request):
    set_search_path()
    top_indonesia = query(
        """
        SELECT id, judul, sinopsis, url_video_trailer, release_date_trailer, total_view
        FROM "TAYANGAN"
        WHERE asal_negara = 'Indonesia'
        ORDER BY total_view DESC
        LIMIT 10
        """
    )
    context = {
        "tayangan": top_indonesia if isinstance(top_indonesia, list) else [],
        "error": top_indonesia if not isinstance(top_indonesia, list) else None,
    }
    return render(request, "tayangan.html", context)

def top_global(request):
    set_search_path()
    top_global = query(
        """
        SELECT T.id, T.judul, T.sinopsis, T.url_video_trailer, T.release_date_trailer,
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
        "tayangan": top_global if isinstance(top_global, list) else [],
        "error": top_global if not isinstance(top_global, list) else None,
    }
    return render(request, "tayangan.html", context)
