import sqlite3
import matplotlib.pyplot as plt
import numpy as np

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
        if s[0] != 0:
            avg_speeds.append(s[0])
    return np.array(avg_speeds)
    
db_file = 'tracks.bk'
conn = conn = sqlite3.connect(db_file)
# Columns in track_details_table:
# [ ('_id',), ('Time',), ('Distance',), ('avgSpeed',), ('maxspeed',), 
#   ('date',), ('max_altitude',), ('min_altitude',), ('start_time',), 
#   ('final_alt',), ('initial_alt',), ('calorie_count',), ('note_text',), 
#   ('start_timestamp',), ('elapsed_seconds',), ('finish_timestamp',)]
# Time and avgSpeed are interverted
distances = get_distances(conn)
total_dist = 0
for d in distances:
    total_dist += d
print(f'Total distance: {total_dist / 1000:.3f} km')
avg_speeds = get_avg(conn)

fig, ax = plt.subplots(2,1)
ax[0].plot(avg_speeds, 'r')
ax[0].set_ylabel('avg speed (km/h)', color='r')
ax[0].tick_params('y', colors='r')

ax[1].plot(distances/1000, 'b:')
ax[1].set_ylabel('dist (km)', color='b')
ax[1].tick_params('y', colors='b')
ax[1].set_title(f'Total distance: {total_dist / 1000:.3f} km')

fig.suptitle(f'Tracks stats')
plt.show()
