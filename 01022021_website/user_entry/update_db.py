import psycopg2
conn=psycopg2.connect(host='localhost',database='netala_database',user='postgres',password='Root@1234A')
curr=conn.cursor()
curr.execute("UPDATE user_list SET user_type = 'USER' WHERE user_type = 'user';")
conn.commit()
print('Rows updated:', curr.rowcount)
conn.close()
