import re
def sort_sensor_key(s):
    if s is None: return (9999, 99, "")
    s_upper = s.upper()
    n_match = re.search(r'_N(\d+)', s_upper)
    n_val = int(n_match.group(1)) if n_match else 9999
    
    type_order = 99
    if 'MS1' in s_upper: type_order = 1
    elif 'PH1' in s_upper: type_order = 2
    elif 'PRI' in s_upper or 'PR1' in s_upper: type_order = 3
    elif 'ROI' in s_upper or 'RO1' in s_upper: type_order = 4
    
    return (n_val, type_order, s_upper)

num1 = ['all']
num2 = ['kerela_n6']
name = 'K-DISC'
tenant_id = 2
allowed_node_ids = ['kerela_n1', 'kerela_n2', 'kerela_n3', 'kerela_n4', 'kerela_n5', 'kerela_n6', 'kerela_n7', 'kerela_n8']
node_id = [n for n in num2 if n in allowed_node_ids]

query = "SELECT DISTINCT sensor_id FROM sensor_info WHERE "
conditions = []
params = []

if tenant_id:
    conditions.append("tenant_id = %s")
    params.append(tenant_id)

if len(num1) != 0 and 'all' not in num1:
    type_placeholders = ','.join(['%s'] * len(num1))
    conditions.append("sensor_type IN (" + type_placeholders + ")")
    params.extend(num1)

if len(node_id) != 0:
    node_placeholders = ','.join(['%s'] * len(node_id))
    conditions.append("node_id IN (" + node_placeholders + ")")
    params.extend(node_id)

query += " AND ".join(conditions)

import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cursor=conn.cursor()
cursor.execute(query, params)
node_records = cursor.fetchall()
print("node_records:", node_records)

sensor_id=[]
for row in node_records:
    for col in row:
        sensor_id.append(col)

sensor_id.sort(key=sort_sensor_key)
print("sorted sensor_id:", sensor_id)
