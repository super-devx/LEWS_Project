import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()
cur.execute("SELECT node_id, tenant_id FROM sensor_info LIMIT 20")
print("sensor_info:", cur.fetchall())
cur.execute("SELECT email_id, tenant_id FROM user_list LIMIT 10")
print("user_list:", cur.fetchall())
