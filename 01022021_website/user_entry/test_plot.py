import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

num_sensors = 6
num_cols = 2
num_rows = (num_sensors + num_cols - 1)  # 6 + 2 - 1 = 7

fig_width = 8 * num_cols
fig_height = 6 * num_rows

figure, axes = plt.subplots(num_rows, num_cols, figsize=(fig_width, fig_height))

counter = 0
for i in range(num_sensors):
    rows = counter // num_cols
    cols = counter // num_cols # WAIT! cols = counter % num_cols in the code
    ax = axes[rows, cols] # wait, look at my script, let me check the real code
