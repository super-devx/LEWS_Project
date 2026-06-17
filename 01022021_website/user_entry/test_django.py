import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LEWS_Project.settings')
django.setup()

client = Client()
# We need to simulate the login first to set the 'name' global variable
client.post('/login', {'email': 'K-DISC', 'password': 'password'})

# Now post to fetch_info
response = client.post('/fetch_info', {
    'val': 'browser',
    'st': ['all'],
    'loc': ['kerela_n6']
})

print(response.status_code)
content = response.content.decode('utf-8')
if 'Select Specific Sensors' in content:
    print('Rendered sensor-data-selection.html')
    # Check if sensors are present
    if 'kerela_n6_ms1' in content:
        print('Sensor kerela_n6_ms1 is present in the HTML!')
    else:
        print('Sensors are MISSING from the HTML!')
        # Let's see what is inside checkbox-grid
        import re
        grid_content = re.search(r'<div class="checkbox-grid">([\s\S]*?)</div>', content)
        if grid_content:
            print('Checkbox grid content:', grid_content.group(1).strip())
else:
    print('Did not render sensor-data-selection.html')
