import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

# Columns in track_details_table:
# [ ('_id',), ('Time',), ('Distance',), ('avgSpeed',), ('maxspeed',), 
#   ('date',), ('max_altitude',), ('min_altitude',), ('start_time',), 
#   ('final_alt',), ('initial_alt',), ('calorie_count',), ('note_text',), 
#   ('start_timestamp',), ('elapsed_seconds',), ('finish_timestamp',)]
# Time and avgSpeed are interverted

def cleanup_table(conn):
    """ Remove incomplete tracks where average speed is 0 """
    cur = conn.cursor()
    cur.execute('SELECT * from track_details_table')
    for row in cur.fetchall():
        if row[1] == 0:
            row_id = row[0]
            cur.execute(f'DELETE from track_details_table where _id = {row_id}')
    return conn    

def get_distances(conn):
    cur = conn.cursor()
    cur.execute('SELECT Distance from track_details_table')
    dists = []
    for d in cur.fetchall():
        if d[0] != 0:
            dists.append(d[0])
    return np.array(dists)

def get_avg(conn):
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
    
db_file = 'tracks.bk'
conn = sqlite3.connect(db_file)
conn = cleanup_table(conn)
avg_speeds = get_avg(conn)
distances = get_distances(conn)
timestamps = get_start_timestamps(conn)
total_dist = 0
for d in distances:
    total_dist += d
print(f'Total distance: {total_dist / 1000:.3f} km')

fig, ax = plt.subplots(2,1, figsize=(7,6.5))
ax[0].plot(timestamps, avg_speeds, 'r-o')
ax[0].set_ylabel('km/h', color='r')
ax[0].tick_params('y', colors='r')
ax[0].set_title(f'Average speed')

ax[1].plot(timestamps, distances/1000, 'b:x')
ax[1].set_ylabel('km', color='b')
ax[1].tick_params('y', colors='b')
ax[1].set_title(f'Distance (total : {total_dist / 1000:.3f} km)')

fig.autofmt_xdate()
ax[0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

fig.suptitle(f'Tracks stats')
plt.show()
