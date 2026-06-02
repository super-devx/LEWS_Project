import os
import django
import sys
import matplotlib
matplotlib.use('Agg')
import re
import base64

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_entry.settings')
django.setup()

from django.test import RequestFactory
from login.views import secondPartNew

rf = RequestFactory()
request = rf.post('/add', {
    'sensor_list_id': ['kerala_n2_ms1', 'kerala_n3_pr1'],
    'from_date': '2026-03-22',
    'to_date': '2026-06-02',
    'from_hr': '00',
    'from_min': '00',
    'to_hr': '23',
    'to_min': '59',
    'chart_type': 'timeseries',
    'duration': '168',
    'query_type': '1'
})

response = secondPartNew(request)
content = response.content.decode('utf-8')
match = re.search(r'data:image/png;base64,([^\'"]+)', content)
if match:
    img_data = match.group(1)
    with open('test_output.png', 'wb') as f:
        f.write(base64.b64decode(img_data))
    print("Graph saved to test_output.png")
else:
    print("No graph found in response!")
