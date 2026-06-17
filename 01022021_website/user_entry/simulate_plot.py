import os
import django
import sys
import matplotlib
matplotlib.use('Agg')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_entry.settings')
django.setup()

from login.views import firstPart, tempData, queryExec, setData, sensorDict
import datetime
import matplotlib.pyplot as plt

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
q = firstPart(request)
node_records = queryExec(q)
data = setData(node_records)
Dict = sensorDict(data)

drawlist = {}
for i in range(len(Dict.get("sensorid", []))):
    temp_data = tempData(data, Dict["sensorid"][i], i)
    for aa in temp_data:
        dataset = drawlist.get(Dict["sensorid"][i], {})
        x = dataset.get('x', [])
        y = dataset.get('y', [])
        value = aa[0]
        y.append(aa[1])
        x.append(aa[2])
        drawlist[Dict["sensorid"][i]] = {'x': x, 'y': y, 'value': value}

keys = list(drawlist.keys())
print("Keys to plot:", keys)

num_cols = 2
num_rows = (len(Dict["sensorid"]) + num_cols - 1)
fig_width = 8 * num_cols
fig_height = 6 * num_rows
figure, axes = plt.subplots(num_rows, num_cols, figsize=(fig_width, fig_height))

counter = 0
for key in keys:
    rows = counter // num_cols
    cols = counter % num_cols
    ax = axes[rows, cols]
    counter = counter + 1
    data_plot = drawlist[key]
    print(f"Plotting {key} with {len(data_plot['x'])} points")
    ax.plot(data_plot['x'], data_plot['y'])

figure.savefig('test_plot_pitch.png')
print("Saved to test_plot_pitch.png")
