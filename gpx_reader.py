from glob import glob
import gpxpy
import numpy as np
import os

class GpxReader():
    def __init__(self, dir, verbose=False):
        self.dir = dir
        self.verbose = verbose
        all_files = glob(os.path.join(dir, '*'))
        self.gpx_files = []
        for f in all_files:
            if f.lower().endswith('.gpx'):
                self.gpx_files.append(f)
                if self.verbose:
                    print(f)
        self.parse_all_files(self.gpx_files)

    def parse_all_files(self, files):
        self.dists = []
        durations = []
        self.avg_speeds = []
        self.start_timestamps = []
        self.max_speeds = []
        for gpxfile in files:
            with open(gpxfile, 'r') as f:
                gpx = gpxpy.parse(f)
                d_km = gpx.length_2d() / 1000
                t_sec = gpx.get_duration()
                self.dists.append(d_km)
                durations.append(t_sec)
                self.avg_speeds.append(3600 * d_km / t_sec)
                start_time = gpx.get_time_bounds()[0]
                start_time = start_time.replace(tzinfo=None)
                self.start_timestamps.append(start_time)
                moving_data = gpx.get_moving_data()
                self.max_speeds.append(moving_data.max_speed * 3.6)
                if self.verbose:
                    print(f'Start time: {self.start_timestamps[-1]}, distance: {d_km} km, duration: {t_sec} sec, average speed: {self.avg_speeds[-1]}, max speed: {self.max_speeds[-1]}')

    def get_distances_km(self):
        return np.array(self.dists)

    def get_avg_speed_kmh(self):
        return np.array(self.avg_speeds)

    def get_max_speed_kmh(self):
        return max(self.max_speeds)

    def get_start_timestamps(self):
        return self.start_timestamps
