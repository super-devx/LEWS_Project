import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()

# Simulating fetch_info query
num1 = ['moisture']
num2 = ['kerala_n4']
tenant_id = 2

query = "SELECT DISTINCT sensor_id FROM sensor_info WHERE "
conditions = []
params = []

conditions.append("tenant_id = %s")
params.append(tenant_id)

type_placeholders = ','.join(['%s'] * len(num1))
conditions.append("sensor_type IN (" + type_placeholders + ")")
params.extend(num1)

node_placeholders = ','.join(['%s'] * len(num2))
conditions.append("node_id IN (" + node_placeholders + ")")
params.extend(num2)

query += " AND ".join(conditions)
print("Query:", query)
print("Params:", params)
cur.execute(query, params)
records = cur.fetchall()
print("Result:", records)
