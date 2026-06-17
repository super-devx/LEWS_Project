import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()
cur.execute("SELECT COUNT(*) FROM sensor_info WHERE node_id LIKE 'him_node_%'")
print('Himachal sensors in DB:', cur.fetchone()[0])
cur.execute("SELECT node_id, sensor_type FROM sensor_info WHERE node_id LIKE 'sikkim_node_%'")
print('Sikkim sensors in DB:', cur.fetchall())
cur.execute("SELECT node_id FROM node WHERE location='himachal'")
print('Himachal nodes:', cur.fetchall())
