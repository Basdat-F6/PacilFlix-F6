import psycopg2

# Konfigurasi koneksi ke database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres.bbsbckcikdcqglpcrkvq",
    password="bussdeaDkcfg6022",
    host="aws-0-ap-southeast-1.pooler.supabase.com",
    port="5432"
)

cursor = conn.cursor()

# Query untuk mendapatkan daftar tabel
cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'public'")
tables = cursor.fetchall()

print("Daftar tabel dalam skema 'public':")
for table in tables:
    print(table)

# Jika Anda ingin melihat tabel dalam skema tertentu, misalnya 'pacilflix'
cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'pacilflix'")
tables = cursor.fetchall()

print("\nDaftar tabel dalam skema 'pacilflix':")
for table in tables:
    print(table)

cursor.close()
conn.close()
