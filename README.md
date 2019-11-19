# BikeometerStats

## Description

This python script displays stats (total distance, total time, global average speed) and plots average speed and distance of each track.

The data is obtained from the exported tracks.bk file. As of 2019/10/30, Bikeometer has two bugs in data export:
- Time and avgSpeed are interverted in the track_details_table
- The last exported track only contains _id, date and start_timestamp

## Command line arguments

```
> python bikeometer.py --help
usage: bikeometer.py [-h] [-v] [-f FILE]

Plot statistics from Bikeometer exported file.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print table contents.
  -f FILE, --file FILE  Bikeometer exported file.
```

## Example results

```
> python bikeometer.py
Removing track 50 because average speed is 0.
Total distance: 421.245 km.
Total time: 19h06min3s.
Global average speed: 22.05 km/h.
Max speed: 41.78 km/h.
Total kcal: 4079.89 kcal.
Average power: 248.25 W.
```

![alt text](example.png "Output example")
