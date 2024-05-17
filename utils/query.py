import psycopg2, os
from psycopg2 import Error

try:
    connection = psycopg2.connect(user='postgres.bbsbckcikdcqglpcrkvq',
                                password='bussdeaDkcfg6022',
                                host='aws-0-ap-southeast-1.pooler.supabase.com',
                                port='5432',
                                database='postgres')

    cursor = connection.cursor()

    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    cursor.execute("SELECT version();")

    record = cursor.fetchall()
    print("You are connected to - ", record, "\n")
    cursor.execute('SET search_path TO "pacilflix";')

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)