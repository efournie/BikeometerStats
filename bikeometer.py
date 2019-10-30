import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sqlite3

parser = argparse.ArgumentParser(description=f'Plot statistics from Bikeometer exported file.')
parser.add_argument('-v', '--verbose', type=lambda x:(str(x).lower()=='true'), default=False, help='Print table contents.')
parser.add_argument('-f', '--file', type=str, default='tracks.bk', help='Bikeometer exported file.')
args = parser.parse_args()

# Columns in track_details_table:
# [ ('_id',), ('Time',), ('Distance',), ('avgSpeed',), ('maxspeed',), 
#   ('date',), ('max_altitude',), ('min_altitude',), ('start_time',), 
#   ('final_alt',), ('initial_alt',), ('calorie_count',), ('note_text',), 
#   ('start_timestamp',), ('elapsed_seconds',), ('finish_timestamp',)]
# 
# Existing bugs in Bikeometer exported files:
#   - Time and avgSpeed are interverted
#   - The last exported track only contains _id, date and start_timestamp

def cleanup_table(conn):
    ''' Remove incomplete tracks where average speed is 0 '''
    cur = conn.cursor()
    cur.execute('SELECT * from track_details_table')
    for row in cur.fetchall():
        if row[1] == 0:
            row_id = row[0]
            cur.execute(f'DELETE from track_details_table where _id = {row_id}')
            print(f'Removing track {row_id} because average speed is 0.')
    return conn    

def get_distances_km(conn):
    cur = conn.cursor()
    cur.execute('SELECT Distance from track_details_table')
    dists = []
    for d in cur.fetchall():
        if d[0] != 0:
            dists.append(d[0] / 1000)
    return np.array(dists)

def get_avg_speed_kmh(conn):
    cur = conn.cursor()
    # Error : column Time contains average speed
    cur.execute('SELECT Time from track_details_table')
    avg_speeds = []
    for s in cur.fetchall():
        avg_speeds.append(s[0])
    return np.array(avg_speeds)

def get_start_timestamps(conn):
    cur = conn.cursor()
    cur.execute('SELECT start_timestamp from track_details_table')
    times = []
    for t in cur.fetchall():
        times.append(datetime.fromtimestamp(t[0]/1000))
    return times

def print_content(conn):
    cur = conn.cursor()
    cur.execute(f'SELECT name from PRAGMA_TABLE_INFO("track_details_table")')
    rows = cur.fetchall()
    print(rows)
    cur.execute('SELECT * from track_details_table')
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Read from tables
conn = sqlite3.connect(args.file)
if args.verbose:
    print_content(conn)
conn = cleanup_table(conn)
avg_speeds_kmh = get_avg_speed_kmh(conn)
distances_km = get_distances_km(conn)
timestamps = get_start_timestamps(conn)

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
print(f'Total distance: {total_dist_km:.3f} km. Total time: {hours}h{minutes:02d}min{seconds}s. Global average speed: {global_average_speed_kmh:.2f} km/h.')

# Plot results
fig, ax = plt.subplots(2,1, figsize=(7,6.5))
ax[0].plot(timestamps, avg_speeds_kmh, 'r-o')
ax[0].set_ylabel('km/h', color='r')
ax[0].tick_params('y', colors='r')
ax[0].set_title(f'Average speed (global: {global_average_speed_kmh:.2f} km/h)')

ax[1].plot(timestamps, distances_km, 'b:x')
ax[1].set_ylabel('km', color='b')
ax[1].tick_params('y', colors='b')
ax[1].set_title(f'Distance (total : {total_dist_km:.3f} km)')

fig.autofmt_xdate()
ax[0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

fig.suptitle(f'Tracks stats')
plt.show()
