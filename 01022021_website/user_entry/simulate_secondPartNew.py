import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_entry.settings')
django.setup()

from login.views import firstPart, tempData, queryExec, setData, sensorDict
import datetime

class DummyPOST(dict):
    def getlist(self, key):
        return self.get(key, [])

class RequestWrapper:
    def __init__(self):
        self.POST = DummyPOST({
            'sensor_list_id': ['nt_n1_pi2', 'nt_n1_pi3'],
            'from_date': '2020-01-01',
            'to_date': '2026-12-31',
            'from_hr': '00',
            'from_min': '00',
            'to_hr': '23',
            'to_min': '59',
            'chart_type': 'line',
            'duration': '1',
            'query_type': '1'
        })

request = RequestWrapper()
try:
    q = firstPart(request)
except Exception as e:
    print("Exception in firstPart:", e)
    sys.exit(1)
    
if q is None:
    print("firstPart returned None.")
    sys.exit(1)
    
print("QUERY:", q)
node_records = queryExec(q)
print("RECORDS LENGTH:", len(node_records))
data = setData(node_records)
Dict = sensorDict(data)
print("Dict sensorid:", Dict.get("sensorid"))

for i in range(len(Dict.get("sensorid", []))):
    print("Testing sensor:", Dict["sensorid"][i])
    temp_data = tempData(data, Dict["sensorid"][i], i)
    print("Temp Data Length:", len(temp_data))
    if len(temp_data) > 0:
        print("First row:", temp_data[0])
