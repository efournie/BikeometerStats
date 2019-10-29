import sqlite3
import matplotlib.pyplot as plt

def get_distances(conn):
    cur = conn.cursor()
    cur.execute('SELECT Distance from track_details_table')
    rows = cur.fetchall()
    return rows

def get_avg(conn):
    cur = conn.cursor()
    # Error : column Time contains average speed
    cur.execute('SELECT Time from track_details_table')
    avg_speeds = []
    for s in cur.fetchall():
        if s[0] != 0:
            avg_speeds.append(s[0])
    return avg_speeds
    
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
    total_dist += d[0]
print(f'Total distance: {total_dist / 1000:.3f} km')

avg_speeds = get_avg(conn)
plt.plot(avg_speeds)
plt.title('Average speed (km/h)')
plt.show()
