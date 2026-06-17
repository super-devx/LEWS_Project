import psycopg2
conn = psycopg2.connect(user='postgres',password='Root@1234A',host='127.0.0.1',port='5432',database='netala_database')
cursor = conn.cursor()

cursor.execute("SELECT sensor_id FROM sensor_info WHERE sensor_id LIKE 'kerala_%_ph%';")
rows = cursor.fetchall()

updated = 0
for row in rows:
    old_id = row[0]
    new_id = old_id.replace('_ph', '_pi')
    cursor.execute("UPDATE sensor_info SET sensor_id = %s WHERE sensor_id = %s;", (new_id, old_id))
    updated += cursor.rowcount

conn.commit()
print('Rows updated:', updated)
 