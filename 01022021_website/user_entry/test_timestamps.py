import psycopg2
try:
    conn = psycopg2.connect('dbname=netala_database user=postgres password=Root@1234A host=127.0.0.1')
    cursor = conn.cursor()
    cursor.execute("SELECT sensor_id FROM sensor_info WHERE sensor_id ILIKE 'kerala%';")
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    print(e)
