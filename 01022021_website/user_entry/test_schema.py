import psycopg2
conn = psycopg2.connect('dbname=netala_database user=postgres password=Root@1234A host=127.0.0.1')
cursor = conn.cursor()
cursor.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'user_list';")
for row in cursor.fetchall():
    print(row)
