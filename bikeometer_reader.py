from datetime import datetime
import numpy as np
import sqlite3
import sys

class BikeometerReader():
    # Columns in track_details_table:
    # [ ('_id',), ('Time',), ('Distance',), ('avgSpeed',), ('maxspeed',),
    #   ('date',), ('max_altitude',), ('min_altitude',), ('start_time',),
    #   ('final_alt',), ('initial_alt',), ('calorie_count',), ('note_text',),
    #   ('start_timestamp',), ('elapsed_seconds',), ('finish_timestamp',)]
    #
    # Existing bugs in Bikeometer exported files:
    #   - Time and avgSpeed are interverted
    #   - The last exported track only contains _id, date and start_timestamp
    def __init__(self, filename, verbose=False):
        self.conn = sqlite3.connect(filename)
        if verbose:
            self.print_content()
        self.conn = self.cleanup_table()

    def cleanup_table(self):
        ''' Remove incomplete tracks where average speed is 0 '''
        cur = self.conn.cursor()
        cur.execute('SELECT * from track_details_table')
        for row in cur.fetchall():
            if row[1] == 0:
                row_id = row[0]
                cur.execute(f'DELETE from track_details_table where _id = {row_id}')
                print(f'Removing track {row_id} because average speed is 0.', file=sys.stderr)
        return self.conn

    def print_content(self):
        ''' Print SQL table contents '''
        cur = self.conn.cursor()
        cur.execute(f'SELECT name from PRAGMA_TABLE_INFO("track_details_table")')
        rows = cur.fetchall()
        print(rows)
        cur.execute('SELECT * from track_details_table')
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def get_distances_km(self):
        cur = self.conn.cursor()
        cur.execute('SELECT Distance from track_details_table')
        dists = []
        for d in cur.fetchall():
            if d[0] != 0:
                dists.append(d[0] / 1000)
        return np.array(dists)

    def get_avg_speed_kmh(self):
        cur = self.conn.cursor()
        # Error : column Time contains average speed
        cur.execute('SELECT Time from track_details_table')
        avg_speeds = []
        for s in cur.fetchall():
            avg_speeds.append(s[0])
        return np.array(avg_speeds)

    def get_max_speed_kmh(self):
        cur = self.conn.cursor()
        cur.execute('SELECT maxspeed from track_details_table')
        max_speed_kmh = 0
        for s in cur.fetchall():
            if s[0] > max_speed_kmh:
                max_speed_kmh = s[0]
        return max_speed_kmh

    def get_total_kcal(self):
        cur = self.conn.cursor()
        cur.execute('SELECT calorie_count from track_details_table')
        total_kcal = 0
        for s in cur.fetchall():
            total_kcal += s[0]
        return total_kcal

    def get_start_timestamps(self):
        cur = self.conn.cursor()
        cur.execute('SELECT start_timestamp from track_details_table')
        times = []
        for t in cur.fetchall():
            times.append(datetime.fromtimestamp(t[0]/1000))
        return times
