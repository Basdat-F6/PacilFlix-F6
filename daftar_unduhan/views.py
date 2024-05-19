from django.shortcuts import render, redirect
from django.contrib import messages
from utils.query import get_db_connection
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import JsonResponse

def kelola_daftar_unduhan(request):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()

    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
            cursor.execute(
                'SELECT "judul", "timestamp", "id_tayangan" '
                'FROM "TAYANGAN_TERUNDUH", "TAYANGAN" '
                'WHERE "username" = %s AND "id" = "id_tayangan"',
                [username_cookie]
            )
            daftar_unduhan = cursor.fetchall()
        except Exception as error:
            messages.error(request, str(error).split('CONTEXT')[0])
            daftar_unduhan = []
        finally:
            cursor.close()
            connection.close()

    context = {
        'username_cookie': username_cookie,
        'daftar_unduhan': daftar_unduhan,
    }

    if not daftar_unduhan:
        context['tidak_punya_daftar'] = True

    return render(request, 'daftar_unduhan.html', context)

@csrf_exempt
def delete_unduhan(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('id_tayangan')
        username = request.COOKIES.get('username')

        connection, cursor = get_db_connection()

        try:
            # Ambil timestamp saat ini
            current_timestamp = datetime.now()

            # Periksa apakah tayangan telah diunduh lebih dari 1 hari yang lalu
            cursor.execute('SELECT "timestamp" FROM "TAYANGAN_TERUNDUH" WHERE "id_tayangan" = %s AND "username" = %s', [id_tayangan, username])
            unduhan_row = cursor.fetchone()
            if unduhan_row:
                unduhan_timestamp = unduhan_row[0]
                if (current_timestamp - unduhan_timestamp) < timedelta(days=1):
                    return JsonResponse({'success': False, 'message': 'Tayangan tidak dapat dihapus karena belum terunduh lebih dari 1 hari'}, status=400)
                else:
                    cursor.execute('DELETE FROM "TAYANGAN_TERUNDUH" WHERE "id_tayangan" = %s AND "username" = %s ', [id_tayangan, username])
                    connection.commit()
                    return JsonResponse({'success': True, 'message': 'Tayangan berhasil dihapus'})
            else:
                return JsonResponse({'success': False, 'message': 'Tayangan tidak ditemukan'}, status=404)
            
        except Exception as e:
            # Tangani kesalahan jika terjadi
            print(f"Error deleting data from database: {e}")
            connection.rollback()
            return JsonResponse({'success': False, 'message': 'Terjadi kesalahan saat menghapus tayangan'}, status=500)
        finally:
            # Tutup koneksi database
            cursor.close()
            connection.close()

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


from django.shortcuts import render, redirect
from django.contrib import messages
from utils.query import get_db_connection
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse

@csrf_exempt
def unduh(request):
    if request.method == 'POST':
        id_tayangan = request.POST.get('idTayangan')
        username = request.COOKIES.get('username')

        connection, cursor = get_db_connection()
        try:
            cursor.execute('SELECT * FROM "TAYANGAN_TERUNDUH" WHERE "id_tayangan" = %s AND "username" = %s', (id_tayangan, username))
            already_downloaded = cursor.fetchone()
            if already_downloaded:
                return JsonResponse({'success': False, 'message': 'Anda sudah mengunduh tayangan ini'}, status=400)
            else:
                timestamp = datetime.now()
                cursor.execute('INSERT INTO "TAYANGAN_TERUNDUH" ("id_tayangan", "timestamp", "username") VALUES (%s, %s, %s)', (id_tayangan, timestamp, username))
                connection.commit()
                return JsonResponse({'success': True, 'message': 'Tayangan berhasil diunduh'})
        except Exception as e:
            print(f"Error inserting data into database: {e}")
            connection.rollback()
            return JsonResponse({'success': False, 'message': 'Terjadi kesalahan saat mengunduh tayangan'}, status=500)
        finally:
            cursor.close()
            connection.close()

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
