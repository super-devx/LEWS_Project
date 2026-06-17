import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_entry.settings")
django.setup()

import psycopg2
conn = psycopg2.connect('dbname=netala_database user=postgres password=Root@1234A host=127.0.0.1')
cursor = conn.cursor()

name = "Test User"
email = "testuser@example.com"
ph_no = "9876543210"
password = "Test@123"
utype = "RESEARCHER"

try:
    print("Testing insert 1")
    query="insert into user_list(uname, upassword, ph_no, email_id, user_type, status, verify, tenant_id) values(%s, %s, %s, %s, %s, 'unaccepted', 'no', 1)"
    cursor.execute(query, [name, password, ph_no, email, utype])
    conn.commit()
    print("Insert 1 successful!")
except Exception as e:
    print("Insert 1 failed:", e)

