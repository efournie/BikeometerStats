import argparse
from datetime import datetime
import gpxpy
import os
import sqlite3

parser = argparse.ArgumentParser(description=f'Extract contents of .bk file to .gpx files in a directory.')
parser.add_argument('-b', '--bk', type=str, default='', help='Bikeometer exported file that will be used as input.')
parser.add_argument('-g', '--gpx', type=str, default='', help="Directory in which all output GPX files will be stored.")
args = parser.parse_args()

assert ((args.bk != '') and (args.gpx != '')), 'Both input file and output directory must be set.'

conn = sqlite3.connect(args.bk)
cur = conn.cursor()
cur.execute('SELECT trip_id from location_array')
trip_ids = []
for trip in cur.fetchall():
    if trip[0] not in trip_ids and trip[0] != -1:
        trip_ids.append(trip[0])

for trip in trip_ids:
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    cur.execute(f'SELECT * from location_array where trip_id = {trip} and is_un_paused = 0 and speed != 0')
    for waypoints in cur.fetchall():
        _id = waypoints[0]
        lat = waypoints[1]
        lng = waypoints[2]
        alt = waypoints[3]
        speed = waypoints[4]
        timestamp = datetime.fromtimestamp(waypoints[5]/1000)
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lng, alt, timestamp))
    filename = os.path.join(args.gpx, f'track_{trip:06d}.gpx')
    with open(filename, 'w') as gpxfile:
        gpxfile.write(gpx.to_xml())
