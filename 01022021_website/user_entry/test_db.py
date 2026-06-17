import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()
cur.execute("SELECT email_id, tenant_id FROM user_list")
print('user_list:', cur.fetchall())
cur.execute("SELECT tenant_id, sensor_id FROM sensor_info WHERE node_id='kerela_n6'")
print('sensor_info for N6:', cur.fetchall())
