import requests

url = 'http://127.0.0.1:8000/fetch_info'
data = {
    'val': 'browser',
    'st': ['moisture'],
    'loc': ['kerala_n4']
}
# We need to simulate the session? Wait, name is a global variable.
# We first need to login.
s = requests.Session()
login_data = {
    'uname': 'K-DISC',
    'psw': 'Kerala@123'
}
s.post('http://127.0.0.1:8000/home', data=login_data)
res = s.post(url, data=data)
print(res.status_code)
if 'No sensors found' in res.text:
    print("FOUND BUG!")
else:
    print("WORKED FINE!")
