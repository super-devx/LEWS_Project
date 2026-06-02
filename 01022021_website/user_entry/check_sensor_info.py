import psycopg2
conn = psycopg2.connect(user='postgres',password='Root@1234A',host='127.0.0.1',port='5432',database='netala_database')
cur = conn.cursor()
cur.execute("SELECT * FROM sensor_info WHERE node_id LIKE 'him_node_%'")
print(cur.fetchall())
