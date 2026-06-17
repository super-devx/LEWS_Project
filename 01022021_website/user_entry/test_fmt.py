import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

fig, ax = plt.subplots(figsize=(8,6))
dates = [datetime(2026, 3, 22) + timedelta(days=i) for i in range(70)]
ax.plot(dates, range(70))

# Try setting the EXACT formatter we have in views.py
formatter = mdates.DateFormatter("%d\n%m\n%Y")
locator = mdates.HourLocator(interval=24)

ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_major_locator(locator)

fig.savefig('test_kerala_dates.png')
