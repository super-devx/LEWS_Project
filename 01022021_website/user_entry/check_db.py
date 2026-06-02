import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()
cur.execute("SELECT DISTINCT node_id FROM sensor_info")
print("node_ids in sensor_info:", [r[0] for r in cur.fetchall()])
cur.execute("SELECT DISTINCT node_id FROM node")
print("node_ids in node:", [r[0] for r in cur.fetchall()])
