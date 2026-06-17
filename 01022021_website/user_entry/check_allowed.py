import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
cur=conn.cursor()

name = 'K-DISC' # The logged in user
tenant_id = 2

allowed_nodes_query = """
SELECT DISTINCT node.node_id FROM node
INNER JOIN u_status ON node.location = u_status.location
WHERE u_status.email_id = %s
"""
if tenant_id:
    allowed_nodes_query += " AND node.tenant_id = %s"
    cur.execute(allowed_nodes_query, (name, tenant_id))
else:
    cur.execute(allowed_nodes_query, (name,))

allowed_nodes_result = cur.fetchall()
allowed_node_ids = [row[0] for row in allowed_nodes_result]
print("allowed_node_ids:", allowed_node_ids)
