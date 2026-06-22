import pandas as pd
import numpy as np

df = pd.DataFrame({
    'time': [pd.Timestamp('2023-01-01'), pd.NaT, pd.Timestamp('2023-01-03')],
    'val': [1.0, 2.0, 3.0]
})
df.set_index('time', inplace=True)
try:
    df = df.interpolate(method='time')
    print("Success")
except Exception as e:
    print(f"Exception: {type(e).__name__} - {e}")
