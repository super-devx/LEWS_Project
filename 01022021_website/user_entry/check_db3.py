import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()
cur.execute("SELECT tenant_id, COUNT(*) FROM sensor_info GROUP BY tenant_id")
print("sensor_info tenants:", cur.fetchall())
cur.execute("SELECT tenant_id, COUNT(*) FROM user_list GROUP BY tenant_id")
print("user_list tenants:", cur.fetchall())
