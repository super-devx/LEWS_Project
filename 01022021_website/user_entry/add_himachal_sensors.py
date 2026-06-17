import psycopg2

conn = psycopg2.connect(user='postgres',password='Root@1234A',host='127.0.0.1',port='5432',database='netala_database')
cur = conn.cursor()

# First delete any existing himachal sensors just in case
cur.execute("DELETE FROM sensor_info WHERE node_id LIKE 'him_node_%'")

# Insert standard sensors for him_node_1 through him_node_5
sensor_types = {
    'ms1': ('moisture', 'H.P. Moisture'),
    'ph1': ('pitch', 'H.P. Pitch'),
    'pr1': ('pressure', 'H.P. Pressure'),
    'ro1': ('roll', 'H.P. Roll')
}

for i in range(1, 6):
    node_id = f"him_node_{i}"
    
    for s_suffix, (s_type, s_remark) in sensor_types.items():
        sensor_id = f"{node_id}_{s_suffix}"
        # insert into sensor_info
        # columns: sensor_id, sensor_type, remark, node_id, tenant_id
        cur.execute(
            "INSERT INTO sensor_info (sensor_id, sensor_type, remark, node_id, tenant_id) VALUES (%s, %s, %s, %s, %s)",
            (sensor_id, s_type, s_remark, node_id, 1)
        )

conn.commit()
print("Himachal sensors inserted successfully")
