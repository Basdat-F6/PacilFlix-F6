# from django.shortcuts import render, redirect
# from django.contrib import messages
# from utils.query import get_db_connection
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from datetime import datetime, timedelta

# def kelola_daftar_favorit(request):
#     username_cookie = request.COOKIES.get('username')
#     connection, cursor = get_db_connection()

#     if connection is None or cursor is None:
#         messages.error(request, 'Database connection failed')
#     else:
#         try:
#             cursor.execute('SELECT "judul", "timestamp" FROM "DAFTAR_FAVORIT" WHERE "username" = %s', [username_cookie])
#             daftar_favorit = cursor.fetchall()
#         except Exception as error:
#             messages.error(request, str(error).split('CONTEXT')[0])
#             daftar_favorit = []
#         finally:
#             cursor.close()
#             connection.close()

#         context = {
#             'username_cookie': username_cookie,
#             'daftar_favorit': daftar_favorit,
#         }

#         if not daftar_favorit:
#             context['tidak_punya_daftar'] = True

#         return render(request, 'daftar_favorit.html', context)

# def detail_daftar(request, judul):
#     username_cookie = request.COOKIES.get('username')
#     connection, cursor = get_db_connection()

#     if connection is None or cursor is None:
#         messages.error(request, 'Database connection failed')
#     else:
#         try:
#             cursor.execute("""
#                 SELECT DISTINCT t."judul", td."id_tayangan"
#                 FROM "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" td
#                 JOIN "DAFTAR_FAVORIT" df ON td."username" = df."username"
#                 JOIN "TAYANGAN" t ON td."id_tayangan" = t."id"
#                 WHERE df."username" = %s AND df.judul = %s AND df."timestamp" = td."timestamp"
#             """, [username_cookie, judul])
#             daftar_tayangan = cursor.fetchall()
#             print(daftar_tayangan)
#         except Exception as error:
#             messages.error(request, str(error).split('CONTEXT')[0])
#             daftar_tayangan = []
#         finally:
#             cursor.close()
#             connection.close()

#         context = {
#             'username_cookie': username_cookie,
#             'daftar_tayangan': daftar_tayangan,
#             'judul_daftar': judul,
#         }
#         return render(request, 'detail_daftar.html', context)

# @csrf_exempt    
# def delete_tayangan(request):
#     if request.method == 'POST':
#         id_tayangan = request.POST.get('id_tayangan')
#         username_cookie = request.COOKIES.get('username')
#         connection, cursor = get_db_connection()

#         if connection is None or cursor is None:
#             messages.error(request, 'Database connection failed')
#         else:
#             try: 
#                 cursor.execute('DELETE FROM "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" WHERE "id_tayangan" = %s AND "username" = %s', [id_tayangan, username_cookie])
#                 connection.commit()
#             except Exception as error:
#                 messages.error(request, f'Terjadi kesalahan {error}')
#             finally:
#                 cursor.close()
#                 connection.close()
#         return redirect('daftar_favorit:kelola_daftar_favorit')

# @csrf_exempt
# def delete_daftar(request):
#     if request.method == 'POST':
#         judul = request.POST.get('judul')
#         username_cookie = request.COOKIES.get('username')
#         connection, cursor = get_db_connection()

#         if connection is None or cursor is None:
#             messages.error(request, 'Database connection failed')

#         try:
#             cursor.execute('DELETE FROM "DAFTAR_FAVORIT" WHERE "judul" = %s AND "username" = %s', [judul, username_cookie])
#             connection.commit()
#         except Exception as error:
#             messages.error(request, f'Terjadi kesalahan {error}')
#         finally:
#             cursor.close()
#             connection.close()
#         return redirect('daftar_favorit:kelola_daftar_favorit')

# # @csrf_exempt
# # def add(request):
# #     if request.method == 'POST':
# #         id_tayangan = request.POST.get('idfilm')
# #         data = request.POST.get('timestamp')
# #         data_time = request.POST.get('timestamp').replace('a.m.', 'AM').replace('p.m.', 'PM')
# #         username = request.COOKIES.get('username')
# #         print(data)

# #         # Check if all required data is provided
# #         if not id_tayangan or not data_time or not username:
# #             return JsonResponse({'success': False, 'message': 'Data tidak lengkap'}, status=400)
        
# #         # Parse and format the timestamp
# #         try:
# #             timestamp = datetime.strptime(data_time, '%B %d, %Y, %I:%M %p')
# #             formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
# #         except ValueError as e:
# #             return JsonResponse({'success': False, 'message': f'Error in timestamp format: {e}'}, status=400)
        
# #         connection, cursor = get_db_connection()

# #         if connection is None or cursor is None:
# #             return JsonResponse({'success': False, 'message': 'Gagal terhubung dengan database'}, status=500)
# #         else:
# #             try:
# #                 # Check if the record already exists
# #                 cursor.execute(
# #                     'SELECT * FROM "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" WHERE "id_tayangan" = %s AND "username" = %s',
# #                     (id_tayangan, username)
# #                 )
# #                 already_added = cursor.fetchone()
# #                 if already_added:
# #                     return JsonResponse({'success': False, 'message': 'Anda sudah menambahkan tayangan ini'}, status=400)
# #                 else:
# #                     cursor.execute(
# #                         'INSERT INTO "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" ("id_tayangan", "username", "timestamp") VALUES (%s, %s, %s)',
# #                         (id_tayangan, username, formatted_timestamp)
# #                     )
# #                     connection.commit()
# #                     return JsonResponse({'success': True, 'message': 'Tayangan berhasil ditambahkan'})
# #             except Exception as e:
# #                 connection.rollback()
# #                 print(f"Error inserting data into database: {e}")
# #                 return JsonResponse({'success': False, 'message': 'Terjadi kesalahan.'}, status=500)
# #             finally:
# #                 cursor.close()
# #                 connection.close()

# #     return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

from django.shortcuts import render, redirect
from django.contrib import messages
from utils.query import get_db_connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime, timedelta

def kelola_daftar_favorit(request):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()

    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
            cursor.execute('SELECT "judul", "timestamp" FROM "DAFTAR_FAVORIT" WHERE "username" = %s', [username_cookie])
            daftar_favorit = cursor.fetchall()
        except Exception as error:
            messages.error(request, str(error).split('CONTEXT')[0])
            daftar_favorit = []
        finally:
            cursor.close()
            connection.close()

        context = {
            'username_cookie': username_cookie,
            'daftar_favorit': daftar_favorit,
        }

        if not daftar_favorit:
            context['tidak_punya_daftar'] = True

        return render(request, 'daftar_favorit.html', context)

def detail_daftar(request, judul):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()

    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
            cursor.execute("""
                SELECT DISTINCT t."judul", td."id_tayangan"
                FROM "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" td
                JOIN "DAFTAR_FAVORIT" df ON td."username" = df."username"
                JOIN "TAYANGAN" t ON td."id_tayangan" = t."id"
                WHERE df."username" = %s AND df.judul = %s AND df."timestamp" = td."timestamp"
            """, [username_cookie, judul])
            daftar_tayangan = cursor.fetchall()
            print(daftar_tayangan)
        except Exception as error:
            messages.error(request, str(error).split('CONTEXT')[0])
            daftar_tayangan = []
        finally:
            cursor.close()
            connection.close()

        context = {
            'username_cookie': username_cookie,
            'daftar_tayangan': daftar_tayangan,
            'judul_daftar': judul,
        }
        return render(request, 'detail_daftar.html', context)

@csrf_exempt    
def delete_tayangan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
        username_cookie = request.COOKIES.get('username')
        connection, cursor = get_db_connection()

        if connection is None or cursor is None:
            messages.error(request, 'Database connection failed')
        else:
            try: 
                cursor.execute('DELETE FROM "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" WHERE "id_tayangan" = %s AND "username" = %s', [id_tayangan, username_cookie])
                connection.commit()
            except Exception as error:
                messages.error(request, f'Terjadi kesalahan {error}')
            finally:
                cursor.close()
                connection.close()
        return redirect('daftar_favorit:kelola_daftar_favorit')

@csrf_exempt
def delete_daftar(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        username_cookie = request.COOKIES.get('username')
        connection, cursor = get_db_connection()

        if connection is None or cursor is None:
            messages.error(request, 'Database connection failed')

        try:
            cursor.execute('DELETE FROM "DAFTAR_FAVORIT" WHERE "judul" = %s AND "username" = %s', [judul, username_cookie])
            connection.commit()
        except Exception as error:
            messages.error(request, f'Terjadi kesalahan {error}')
        finally:
            cursor.close()
            connection.close()
        return redirect('daftar_favorit:kelola_daftar_favorit')
@csrf_exempt
def add(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('idfilm')
        data_time = request.POST.get('timestamp').replace('a.m.', 'AM').replace('p.m.', 'PM')
        timestamp =datetime.strptime(data_time, '%B %d, %Y, %I:%M %p')
        username = request.COOKIES.get('username')

        connection, cursor = get_db_connection()
        try:
            cursor.execute('SELECT * FROM "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" WHERE "id_tayangan" = %s AND "username" = %s AND "timestamp" = %s', (id_tayangan, username, timestamp))
            already_added = cursor.fetchone()
            if already_added:
                return JsonResponse({'success': False, 'message': 'Anda sudah menambahkan tayangan ini'}, status=400)
            else:
                cursor.execute('INSERT INTO "TAYANGAN_MEMILIKI_DAFTAR_FAVORIT" ("id_tayangan", "timestamp", "username") VALUES (%s, %s, %s)', (id_tayangan, timestamp, username))
                connection.commit()
                return JsonResponse({'success': True, 'message': 'Tayangan berhasil ditambahkan'})
        except Exception as e:
            print(f"Error inserting data into database: {e}")
            connection.rollback()
            return JsonResponse({'success': False, 'message': 'Terjadi kesalahan.'}, status=500)
        finally:
            cursor.close()
            connection.close()

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)