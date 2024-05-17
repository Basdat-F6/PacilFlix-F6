from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from collections import namedtuple
from django.utils import timezone
from datetime import datetime



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
    username_cookie = request.COOKIES.get('username')

    # Ambil semua tayangan
    tayangan = query(
        """
        SELECT id, judul, sinopsis, url_video_trailer, release_date_trailer
        FROM "TAYANGAN"
        ORDER BY judul
        LIMIT 10
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
        "username_cookie": username_cookie,
        "tayangan": tayangan if isinstance(tayangan, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": tayangan if not isinstance(tayangan, list) else None,
    }
    print(context)
    return render(request, "tayangan.html", context)

def search(request):
    set_search_path()
    username_cookie = request.COOKIES.get('username')
    query_str = request.GET.get("q", "")
    results = query(
        """
        SELECT id, judul, sinopsis, url_video_trailer, release_date_trailer
        FROM "TAYANGAN"
        WHERE judul ILIKE %s
        """, [f"%{query_str}%"]
    )
    context = {
        "username_cookie": username_cookie,
        "results": results if isinstance(results, list) else [],
        "error": results if not isinstance(results, list) else None,
    }
    return render(request, "hasil.html", context)

def top_global(request):
    set_search_path()
    username_cookie = request.COOKIES.get('username')

    # Ambil 10 tayangan terbaik global selama 7 hari terakhir
    top_global = query(
        """
        SELECT T.id, T.judul, T.sinopsis, T.url_video_trailer, T.release_date_trailer,
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
        "username_cookie": username_cookie,
        "tayangan": top_global if isinstance(top_global, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": top_global if not isinstance(top_global, list) else None,
        "is_subscribed": cek_paket_aktif(request),
    }

    return render(request, "tayangan.html", context)

def top_indonesia(request):
    set_search_path()
    username_cookie = request.COOKIES.get('username')

    # Ambil 10 tayangan terbaik di Indonesia selama 7 hari terakhir
    top_indonesia = query(
        """
        SELECT T.id, T.judul, T.sinopsis, T.url_video_trailer, T.release_date_trailer,
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
        "username_cookie": username_cookie,
        "tayangan": top_indonesia if isinstance(top_indonesia, list) else [],
        "film": film if isinstance(film, list) else [],
        "series": series if isinstance(series, list) else [],
        "error": top_indonesia if not isinstance(top_indonesia, list) else None,
        "is_subscribed": cek_paket_aktif(request),

    }

    return render(request, "tayangan.html", context)


def watch_film(request, id_film):
    set_search_path()
    if request.method == "POST":
        watch_progress = int(request.POST.get('watchProgress', 0))
        watch_progress_int = int(request.POST.get('watchProgressInt', 0))
        progress = max(watch_progress, watch_progress_int)
        username_cookie = request.COOKIES.get('username')
        end_date_time = timezone.now()

        # Ambil durasi film
        durasi_film_query = query(
            """
            SELECT durasi_film
            FROM "FILM"
            WHERE id_tayangan = %s
            """, [str(id_film)]
        )

        if durasi_film_query:
            durasi_film = durasi_film_query[0].durasi_film
            durasi_tonton = (progress / 100) * durasi_film
            start_date_time = end_date_time - timezone.timedelta(minutes=durasi_tonton)

            if progress >= 70:  # Simulasi: progress >= 70 berarti user sudah menonton 70% dari durasi
                query(
                    """
                    INSERT INTO "RIWAYAT_NONTON" (id_tayangan, username, start_date_time, end_date_time)
                    VALUES (%s, %s, %s, %s)
                    """, [str(id_film), username_cookie, start_date_time, end_date_time]
                )

        return redirect('tayangan:detail-film', id=id_film)

    return HttpResponse("Invalid method", status=405)



def detail_episode(request, id_series, sub_judul):
    set_search_path()
    username_cookie = request.COOKIES.get('username')

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
        """, [id_series]
    )

    episodes = query(
        """
        SELECT E.id_series, E.sub_judul, E.sinopsis, E.durasi, E.url_video, E.release_date
        FROM "EPISODE" E
        WHERE E.id_series = %s
        ORDER BY E.release_date
        """, [id_series]
    )

    episode = query(
        """
        SELECT E.id_series, E.sub_judul, E.sinopsis, E.durasi, E.url_video, E.release_date
        FROM "EPISODE" E
        WHERE E.id_series = %s AND E.sub_judul = %s
        """, [id_series, sub_judul]
    )

    progress = query(
        """
        SELECT start_date_time, end_date_time
        FROM "RIWAYAT_NONTON"
        WHERE id_tayangan = %s AND username = %s
        ORDER BY end_date_time DESC
        LIMIT 1
        """, [id_series, username_cookie]
    )

    context = {
        "username_cookie": username_cookie,
        "detail": detail[0] if detail else None,
        "episode": episode[0] if episode else None,
        "episodes": episodes if isinstance(episodes, list) else [],
        "progress": progress[0] if progress else None,
        "error": detail if not detail else None,
    }
    return render(request, "episode.html", context)

def watch_episode(request, id_series, sub_judul):
    set_search_path()
    if request.method == "POST":
        watch_progress = int(request.POST.get('watchProgress', 0))
        watch_progress_int = int(request.POST.get('watchProgressInt', 0))
        progress = max(watch_progress, watch_progress_int)
        username_cookie = request.COOKIES.get('username')
        end_date_time = timezone.now()

        episode = query(
            """
            SELECT durasi
            FROM "EPISODE"
            WHERE id_series = %s AND sub_judul = %s
            """, [id_series, sub_judul]
        )
        if episode:
            durasi = episode[0].durasi
            start_date_time = end_date_time - timezone.timedelta(minutes=(progress / 100 * durasi))
            
            query(
                """
                INSERT INTO "RIWAYAT_NONTON" (id_tayangan, username, start_date_time, end_date_time)
                VALUES (%s, %s, %s, %s)
                """, [str(id_series), username_cookie, start_date_time, end_date_time]
            )
        return redirect('tayangan:detail-episode', id_series=id_series, sub_judul=sub_judul)

    return HttpResponse("Invalid method", status=405)


def detail_series(request, id):
    set_search_path()

    username_cookie = request.COOKIES.get('username')
    if not username_cookie:
        return redirect('login')

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

    # Query untuk mengambil data episode terkait series ini
    episodes = query(
        """
        SELECT E.id_series, E.sub_judul, E.sinopsis, E.durasi, E.url_video, E.release_date
        FROM "EPISODE" E
        WHERE E.id_series = %s
        ORDER BY E.release_date
        """, [id]
    )

    # Query untuk mengambil progress watch
    progress = query(
        """
        SELECT start_date_time, end_date_time
        FROM "RIWAYAT_NONTON"
        WHERE id_tayangan = %s AND username = %s
        """, [id, username_cookie]
    )

    if not detail:
        return HttpResponse("Detail not found", status=404)
    detail = detail[0]
    is_released = detail.release_date_trailer <= timezone.now().date()

    context = {
        "username_cookie": username_cookie,
        "detail": detail,
        "episodes": episodes if isinstance(episodes, list) else [],
        "progress": progress if isinstance(progress, list) else [],
        "error": None,
        "is_released": is_released,

    }
    return render(request, "detail_series.html", context)



def detail_film(request, id):
    set_search_path()
    
    username_cookie = request.COOKIES.get('username')
    if not username_cookie:
        return redirect('login')

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

    # Query untuk mendapatkan data progress menonton
    progress = query(
        """
        SELECT start_date_time, end_date_time
        FROM "RIWAYAT_NONTON"
        WHERE id_tayangan = %s AND username = %s
        ORDER BY start_date_time DESC
        LIMIT 1
        """, [id, username_cookie]
    )
    detail = detail[0]
    is_released = detail.release_date_trailer <= timezone.now().date()

    context = {
        "username_cookie": username_cookie,
        "detail": detail,
        "progress": progress[0] if progress else None,
        "error": None,
        "is_released": is_released,

    }
    return render(request, "detail_film.html", context)


def cek_paket_aktif(request):
    set_search_path()
    username_cookie = request.COOKIES.get('username')

    detail = query(
        '''
        SELECT 
            T."nama_paket", 
            P."harga", 
            P."resolusi_layar", 
            STRING_AGG(DP."dukungan_perangkat", ', ') AS dukungan_perangkat,
            T."start_date_time", 
            T."end_date_time",
            T."metode_pembayaran",
            T."timestamp_pembayaran"
        FROM 
            "TRANSACTION" T
        JOIN 
            "PAKET" P ON T."nama_paket" = P."nama"
        LEFT JOIN 
            "DUKUNGAN_PERANGKAT" DP ON T."nama_paket" = DP."nama_paket"
        WHERE 
            T."username" = %s
        GROUP BY 
            T."nama_paket", 
            P."harga", 
            P."resolusi_layar", 
            T."start_date_time", 
            T."end_date_time",
            T."metode_pembayaran",
            T."timestamp_pembayaran";
        ''', [username_cookie]
    )
    is_subsribed = find_date_range(detail, datetime.now()) != None
    return is_subsribed

def find_date_range(date_ranges, input_date):
    if isinstance(input_date, datetime):
        input_date = input_date.date()
    for entry in date_ranges:
        start = entry[4]
        end = entry[5]
        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()
        if start <= input_date <= end:
            return entry
    return None