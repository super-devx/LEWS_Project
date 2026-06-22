import requests

session = requests.Session()
# Get CSRF
r1 = session.get('http://127.0.0.1:8000/signin')
csrf = r1.cookies.get('csrftoken')

print("Attempting login...")
# Mock login (we don't know a valid user, so let's try a dummy one or maybe we don't need to if we just look at the code)
