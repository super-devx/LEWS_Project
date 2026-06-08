import psycopg2
conn = psycopg2.connect('dbname=netala_database user=postgres password=Root@1234A host=127.0.0.1')
cur = conn.cursor()
cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'auth_user');")
print("auth_user exists:", cur.fetchone()[0])
