from django.shortcuts import render, redirect
from utils.query import *
from datetime import datetime, timedelta
from django.contrib import messages 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def show_langganan(request):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
            query = '''
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
                    T."timestamp_pembayaran"
                ORDER BY 
                    T."timestamp_pembayaran" DESC;
            '''
            
            cursor.execute(query, [username_cookie])
            data_transaksi = cursor.fetchall()
            
            langganan_sekarang = find_date_range(data_transaksi, datetime.now())

            cursor.execute('''
                SELECT 
                    p."nama",
                    p."harga",
                    p."resolusi_layar",
                    STRING_AGG(d."dukungan_perangkat", ', ') AS dukungan_perangkat
                FROM 
                    "PAKET" p
                LEFT JOIN 
                    "DUKUNGAN_PERANGKAT" d
                ON 
                    p."nama" = d."nama_paket"
                GROUP BY 
                    p."nama", p."harga", p."resolusi_layar";
                ''')
            
            data_paket = cursor.fetchall()
            context = {
                'username_cookie': username_cookie,
                'data_transaksi': data_transaksi,
                'langganan_sekarang': langganan_sekarang,
                'data_paket': data_paket,
            }
            
            connection.commit()
            return render(request, "langganan.html", context)
        except Exception as error:
            connection.rollback()
            error_message = str(error).split('CONTEXT')[0]
            messages.error(request, error_message)
        finally:
            cursor.close()
            connection.close()

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



def show_beli(request, param_value):
    username_cookie = request.COOKIES.get('username')
    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
    else:
        try:
            query = '''
                SELECT 
                    p."nama",
                    p."harga",
                    p."resolusi_layar",
                    STRING_AGG(d."dukungan_perangkat", ', ') AS dukungan_perangkat
                FROM 
                    "PAKET" p
                LEFT JOIN 
                    "DUKUNGAN_PERANGKAT" d
                ON 
                    p."nama" = d."nama_paket"
                WHERE
                    p."nama" = %s
                GROUP BY 
                    p."nama", p."harga", p."resolusi_layar";
            '''
            
            cursor.execute(query, [param_value])
            data_paket = cursor.fetchone()

            context = {
                'username_cookie': username_cookie,
                'data_paket': data_paket
            }
            
            connection.commit()
            return render(request, "beli.html", context)
        except Exception as error:
            connection.rollback()
            error_message = str(error).split('CONTEXT')[0]
            messages.error(request, error_message)
        finally:
            cursor.close()
            connection.close()

def bayar(request, metode, paket):
    username_cookie = request.COOKIES.get('username')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        messages.error(request, 'Database connection failed')
        return HttpResponseRedirect(reverse('langganan:show_langganan'))
    else:
        try:
            insert_query = '''
                INSERT INTO "TRANSACTION" ("username", "nama_paket", "start_date_time", "end_date_time", "metode_pembayaran", "timestamp_pembayaran")
                VALUES (%s, %s, %s, %s, %s, %s)
            '''

            if metode == 'paypal':
                str_metode = 'PayPal'
            elif metode == 'bank-transfer':
                str_metode = 'Bank Transfer'
            else:
                str_metode = 'Credit Card'

            data_to_insert = (username_cookie, paket, current_time, datetime.now() + timedelta(days=4), str_metode, current_time)
            cursor.execute(insert_query, data_to_insert)
            
            connection.commit()
            return HttpResponseRedirect(reverse('langganan:show_langganan'))
        except Exception as error:
            connection.rollback()
            error_message = str(error).split('CONTEXT')[0]
            messages.error(request, error_message)
            return HttpResponseRedirect(reverse('langganan:show_langganan'))
        finally:
            cursor.close()
            connection.close()
