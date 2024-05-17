from django.shortcuts import render
from utils.query import *

def show_daftar_kontributor(request):
    username_cookie = request.COOKIES.get('username')
    cursor.execute('''
        SELECT
            c."id",
            c."nama",
            STRING_AGG(DISTINCT role, ', ') AS roles,
            c."jenis_kelamin",
            c."kewarganegaraan"
        FROM
            "CONTRIBUTORS" c
        LEFT JOIN (
            SELECT
                p."id",
                'PEMAIN' AS role
            FROM "PEMAIN" p
            UNION ALL
            SELECT
                s."id",
                'SUTRADARA' AS role
            FROM "SUTRADARA" s
            UNION ALL
            SELECT
                ps."id",
                'PENULIS SKENARIO' AS role
            FROM "PENULIS_SKENARIO" ps
        ) roles ON c."id" = roles."id"
        GROUP BY
            c."id";
    ''')
    data_kontributor = cursor.fetchall()
    context = {
        'username_cookie': username_cookie,
        'data_kontributor': data_kontributor
    }
    return render(request, "daftar-kontributor.html", context)

def show_daftar_kontributor_pemain(request):
    username_cookie = request.COOKIES.get('username')
    cursor.execute('''
        SELECT
            c."id",
            c."nama",
            STRING_AGG(DISTINCT role, ', ') AS roles,
            c."jenis_kelamin",
            c."kewarganegaraan"
        FROM
            "CONTRIBUTORS" c
        LEFT JOIN (
            SELECT
                p."id",
                'PEMAIN' AS role
            FROM "PEMAIN" p
            UNION ALL
            SELECT
                s."id",
                'SUTRADARA' AS role
            FROM "SUTRADARA" s
            UNION ALL
            SELECT
                ps."id",
                'PENULIS SKENARIO' AS role
            FROM "PENULIS_SKENARIO" ps
        ) roles ON c."id" = roles."id"
        GROUP BY
            c."id";
    ''')
    data_kontributor = cursor.fetchall()
    context = {
        'username_cookie': username_cookie,
        'data_kontributor': data_kontributor
    }
    return render(request, "pemain-only.html", context)

def show_daftar_kontributor_sutradara(request):
    username_cookie = request.COOKIES.get('username')
    cursor.execute('''
        SELECT
            c."id",
            c."nama",
            STRING_AGG(DISTINCT role, ', ') AS roles,
            c."jenis_kelamin",
            c."kewarganegaraan"
        FROM
            "CONTRIBUTORS" c
        LEFT JOIN (
            SELECT
                p."id",
                'PEMAIN' AS role
            FROM "PEMAIN" p
            UNION ALL
            SELECT
                s."id",
                'SUTRADARA' AS role
            FROM "SUTRADARA" s
            UNION ALL
            SELECT
                ps."id",
                'PENULIS SKENARIO' AS role
            FROM "PENULIS_SKENARIO" ps
        ) roles ON c."id" = roles."id"
        GROUP BY
            c."id";
    ''')
    data_kontributor = cursor.fetchall()
    context = {
        'username_cookie': username_cookie,
        'data_kontributor': data_kontributor
    }
    return render(request, "sutradara-only.html", context)

def show_daftar_kontributor_penulis_skenario(request):
    username_cookie = request.COOKIES.get('username')
    cursor.execute('''
        SELECT
            c."id",
            c."nama",
            STRING_AGG(DISTINCT role, ', ') AS roles,
            c."jenis_kelamin",
            c."kewarganegaraan"
        FROM
            "CONTRIBUTORS" c
        LEFT JOIN (
            SELECT
                p."id",
                'PEMAIN' AS role
            FROM "PEMAIN" p
            UNION ALL
            SELECT
                s."id",
                'SUTRADARA' AS role
            FROM "SUTRADARA" s
            UNION ALL
            SELECT
                ps."id",
                'PENULIS SKENARIO' AS role
            FROM "PENULIS_SKENARIO" ps
        ) roles ON c."id" = roles."id"
        GROUP BY
            c."id";
    ''')
    data_kontributor = cursor.fetchall()
    context = {
        'username_cookie': username_cookie,
        'data_kontributor': data_kontributor
    }
    return render(request, "penulis_skenario-only.html", context)