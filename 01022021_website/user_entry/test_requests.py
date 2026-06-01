import requests

session = requests.Session()
# Don't even need to login properly, just hit fetch_info, but wait, 'name' is global in views.py
# If 'name' is empty in the server process, we can't test it via requests unless we hit login first.
res = session.post('http://127.0.0.1:8000/login_form', data={'email': 'K-DISC', 'password': 'password'})

res = session.post('http://127.0.0.1:8000/fetch_info', data={
    'val': 'browser',
    'st': 'all',
    'loc': 'kerela_n6'
})

content = res.text
if 'Select Specific Sensors' in content:
    print('Rendered sensor-data-selection.html')
    if 'kerela_n6_ms1' in content:
        print('Sensor kerela_n6_ms1 is present in the HTML!')
    else:
        print('Sensors are MISSING from the HTML!')
        import re
        grid_content = re.search(r'<div class="checkbox-grid">([\s\S]*?)</div>', content)
        if grid_content:
            print('Checkbox grid content:', grid_content.group(1).strip())
else:
    print('Did not render sensor-data-selection.html')
