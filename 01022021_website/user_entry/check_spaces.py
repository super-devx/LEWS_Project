import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()

cur.execute("SELECT DISTINCT sensor_type FROM sensor_info")
for r in cur.fetchall():
    print(f"'{r[0]}'", len(r[0]))
