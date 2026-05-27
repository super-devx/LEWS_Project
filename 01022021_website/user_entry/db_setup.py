import psycopg2

conn = psycopg2.connect(user='postgres',password='Root@1234A',host='127.0.0.1',port='5432',database='netala_database')
cur = conn.cursor()

# Delete existing test data if any
cur.execute("DELETE FROM u_status WHERE email_id IN ('sikkim@suhani.com', 'him@suhani.com')")
cur.execute("DELETE FROM user_list WHERE email_id IN ('sikkim@suhani.com', 'him@suhani.com')")
cur.execute("DELETE FROM node WHERE location IN ('sikkim', 'himachal')")

# Sikkim User
sikkim_email = 'sikkim@suhani.com'
cur.execute("INSERT INTO user_list (uname, upassword, ph_no, email_id, user_type, status, verify, tenant_id) VALUES ('Sikkim User', 'iotlab', '0000000000', %s, 'SUPERVISOR', 'accepted', 'True', 1)", (sikkim_email,))
cur.execute("INSERT INTO u_status (email_id, location, tenant_id) VALUES (%s, 'sikkim', 1)", (sikkim_email,))
# Nodes for sikkim (N1 to N4)
for i in range(1, 5):
    node_id = f"sikkim_node_{i}"
    name = f"N{i}"
    cur.execute("INSERT INTO node (name, location, node_id, remark, tenant_id) VALUES (%s, 'sikkim', %s, 'test', 1)", (name, node_id))

# Himachal User
him_email = 'him@suhani.com'
cur.execute("INSERT INTO user_list (uname, upassword, ph_no, email_id, user_type, status, verify, tenant_id) VALUES ('Himachal User', 'iotlab', '1111111111', %s, 'SUPERVISOR', 'accepted', 'True', 1)", (him_email,))
cur.execute("INSERT INTO u_status (email_id, location, tenant_id) VALUES (%s, 'himachal', 1)", (him_email,))
# Nodes for himachal (N1 to N5)
for i in range(1, 6):
    node_id = f"him_node_{i}"
    name = f"N{i}"
    cur.execute("INSERT INTO node (name, location, node_id, remark, tenant_id) VALUES (%s, 'himachal', %s, 'test', 1)", (name, node_id))

conn.commit()
print("Data inserted successfully")
