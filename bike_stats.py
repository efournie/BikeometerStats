import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
from bikeometer_reader import BikeometerReader
from gpx_reader import GpxReader

parser = argparse.ArgumentParser(description=f'Plot statistics from Bikeometer exported data.')
parser.add_argument('-v', '--verbose', action='store_true', help='Print table contents.')
parser.add_argument('-b', '--bk', type=str, default='', help='Bikeometer exported file that will be used as input.')
parser.add_argument('-g', '--gpx', type=str, default='', help="Directory in which all GPX files will be used as input.")
args = parser.parse_args()

assert ((args.bk == '') or (args.gpx == '')) and (args.bk != args.gpx), 'Only one type of input may be used.'

# Read from tables
if args.bk != '':
    bike_data = BikeometerReader(args.bk, args.verbose)
elif args.gpx != '':
    bike_data = GpxReader(args.gpx, args.verbose)

avg_speeds_kmh = bike_data.get_avg_speed_kmh()
distances_km = bike_data.get_distances_km()
timestamps = bike_data.get_start_timestamps()
max_speed_kmh = bike_data.get_max_speed_kmh()
total_kcal = bike_data.get_total_kcal()

avg_speed_evolution = []
total_d = 0
total_t = 0
for d, avg_s in zip(distances_km, avg_speeds_kmh):
    total_d += d
    total_t += d / avg_s
    avg_speed_evolution.append(total_d / total_t)

# Compute some stats
total_dist_km = 0
total_time_h = 0
for n in range(distances_km.shape[0]):
    total_dist_km += distances_km[n]
    total_time_h += distances_km[n] / avg_speeds_kmh[n]
hours = int(total_time_h)
minutes = int((total_time_h - hours) * 60)
seconds = int(((total_time_h - hours) * 60 - minutes) * 60)
global_average_speed_kmh = total_dist_km / total_time_h
power = total_kcal * 4184 / (total_time_h * 3600)

print(f'Total distance: {total_dist_km:.3f} km.')
print(f'Total time: {hours}h{minutes:02d}min{seconds}s.')
print(f'Global average speed: {global_average_speed_kmh:.2f} km/h.')
print(f'Max speed: {max_speed_kmh:.2f} km/h.')
print(f'Total kcal: {total_kcal:.2f} kcal.')
print(f'Average power: {power:.2f} W.')

# Plot results
fig, ax = plt.subplots(2,1, figsize=(7,6.5))
ax[0].plot(timestamps, avg_speeds_kmh, 'r o', label='Average speeds')
ax[0].plot(timestamps, avg_speed_evolution, color='lightcoral', linestyle=':', label='Avg speed evolution')
ax[0].hlines(y=global_average_speed_kmh, xmin=timestamps[0], xmax=timestamps[-1], colors='lightcoral', label='Global avg speed')
ax[0].set_ylabel('km/h', color='r')
ax[0].tick_params('y', colors='r')
ax[0].yaxis.grid()
ax[0].set_title(f'Average speeds (global: {global_average_speed_kmh:.2f} km/h)')
ax[0].legend()

ax[1].plot(timestamps, distances_km, 'b *', label='Distances')
ax[1].set_ylabel('km', color='b')
ax[1].tick_params('y', colors='b')
ax[1].yaxis.grid()
ax[1].set_title(f'Distances (total : {total_dist_km:.3f} km)')
ax[1].legend()

fig.autofmt_xdate()
ax[0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[1].set_xlabel(f'\nTotal time:  {hours}h{minutes:02d}min{seconds}s')

fig.suptitle(f'Tracks stats', fontsize=24)
plt.show()
