import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()
cur.execute("SELECT sensor_id, sensor_type FROM sensor_info WHERE node_id='kerela_n6'")
print(cur.fetchall())
