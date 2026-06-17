import requests

session = requests.Session()
# Login as him@suhani.com
res = session.post('http://127.0.0.1:8000/login_form', data={'email': 'him@suhani.com', 'password': 'iotlab'})

# First check if the session is successfully logged in. In django, the global `name` in views.py will be set.
# Then hit /fetch_info (from first page to second page)
res2 = session.post('http://127.0.0.1:8000/fetch_info', data={
    'val': 'browser',
    'st': 'all',
    'loc': 'him_node_1'
})

content = res2.text
if 'Select Specific Sensors' in content:
    print('Rendered sensor-data-selection.html')
    # Check if the newly added him_node_1 sensors are present
    if 'him_node_1_ms1' in content:
        print('SUCCESS: Sensor him_node_1_ms1 is present in the HTML!')
    else:
        print('FAILED: Sensors are MISSING from the HTML!')
        import re
        grid_content = re.search(r'<div class="checkbox-grid">([\s\S]*?)</div>', content)
        if grid_content:
            print('Checkbox grid content:', grid_content.group(1).strip())
else:
    print('Did not render sensor-data-selection.html')
