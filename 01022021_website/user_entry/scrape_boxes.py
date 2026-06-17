import requests
import re

s = requests.Session()
login_data = {'uname': 'K-DISC', 'psw': 'Kerala@123'}
res1 = s.post('http://127.0.0.1:8000/home', data=login_data)

st_vals = re.findall(r'name=[\'"]st[\'"].*?value=[\'"](.*?)[\'"]', res1.text)
print("st values:", st_vals)

loc_vals = re.findall(r'name=[\'"]loc[\'"].*?value=[\'"](.*?)[\'"]', res1.text)
print("loc values:", loc_vals)
