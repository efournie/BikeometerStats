# BikeometerStats

## Description

`bike_stats.py` displays stats (total distance, total time, global average speed) and plots average speed and distance of each track.

The data is obtained either from the exported `tracks.bk` file (-b argument) or the GPX files contained in the chosen directory (-g argument). 

As of 2019/11/29, Bikeometer has two bugs in data export:
- `Time` and `avgSpeed` are interverted in `track_details_table`
- The last exported track only contains `_id`, `date` and `start_timestamp`

`bk_to_gpx.py` creates GPX files in the chosen directory from the exported .bk file and can be used to export contents of `tracks.bk` in a portable format. Note that there are discrepancies between the tracks data obtained directly from the bk file and the converted GPX files because `gpxpy` eliminates outliers in the GPX files.

## Requirements

Following python libraries are used:
- matplotlib
- numpy
- gpxpy

## Command line arguments

### bike_stats
```
> python bike_stats.py --help
usage: bike_stats.py [-h] [-v] [-b BK] [-g GPX]

Plot statistics from Bikeometer exported data.

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Print table contents.
  -b BK, --bk BK     Bikeometer exported file that will be used as input.
  -g GPX, --gpx GPX  Directory in which all GPX files will be used as input.
```

### bk_to_gpx
```
> python bk_to_gpx.py --help
usage: bk_to_gpx.py [-h] [-b BK] [-g GPX]

Extract contents of .bk file to .gpx files in a directory.

optional arguments:
  -h, --help         show this help message and exit
  -b BK, --bk BK     Bikeometer exported file that will be used as input.
  -g GPX, --gpx GPX  Directory in which all output GPX files will be stored.
  ```

## Example results

```
> python bike_stats.py -b tracks.bk
Removing track 90 because average speed is 0.
Total distance: 841.289 km.
Total time: 36h56min18s.
Global average speed: 22.78 km/h.
Max speed: 46.32 km/h.
Total kcal: 8115.75 kcal.
Average power: 255.35 W.
```

![alt text](example.png "Output example")
