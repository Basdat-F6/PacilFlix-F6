from django.shortcuts import render
from utils.query import *
from django.contrib import messages 

def show_daftar_kontributor(request):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
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
            connection.commit()
            return render(request, "daftar-kontributor.html", context)
        except Exception as error:
            connection.rollback()
            error_message = str(error).split('CONTEXT')[0]
            messages.error(request, error_message)
        finally:
            cursor.close()
            connection.close()

def show_daftar_kontributor_pemain(request):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
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
            connection.commit()
            return render(request, "pemain-only.html", context)
        except Exception as error:
            connection.rollback()
            error_message = str(error).split('CONTEXT')[0]
            messages.error(request, error_message)
        finally:
            cursor.close()
            connection.close()

def show_daftar_kontributor_sutradara(request):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
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
            connection.commit()
            return render(request, "sutradara-only.html", context)
        except Exception as error:
            connection.rollback()
            error_message = str(error).split('CONTEXT')[0]
            messages.error(request, error_message)
        finally:
            cursor.close()
            connection.close()

def show_daftar_kontributor_penulis_skenario(request):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
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
            connection.commit()
            return render(request, "penulis_skenario-only.html", context)
        except Exception as error:
            connection.rollback()
            error_message = str(error).split('CONTEXT')[0]
            messages.error(request, error_message)
        finally:
            cursor.close()
            connection.close()