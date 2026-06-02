import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()
cur.execute("SELECT * FROM sensor_info WHERE node_id='kerala_n4'")
print("kerala_n4 sensors:", cur.fetchall())
cur.execute("SELECT * FROM sensor_info WHERE node_id='kerala_n1'")
print("kerala_n1 sensors:", cur.fetchall())
