#!/usr/bin/env python
import bisect
from argparse import ArgumentParser, FileType
from collections import namedtuple


parser = ArgumentParser()
parser.add_argument('-f', '--file', type=FileType(), required=True)
args = parser.parse_args()

times = []
Time = namedtuple('Time', 'value type')
for line in args.file:
    stime, etime = line.strip().split(',')
    bisect.insort(times, Time(stime, 'starting'))
    bisect.insort(times, Time(etime, 'ending'))

counter, peak, ranges, points = 0, -1, [], {}
prev_time = Time(None, None)
for time in times:
    counter += 1 if time.type == 'starting' else -1
    if time.type == 'starting':
        stime = time
        if counter > peak:
            peak = counter
            ranges = []
    elif counter == peak-1:
        ranges.append((stime.value, time.value))

    if time.value == prev_time.value:
        if time.value in points:
            points[time.value] += 1
        else:
            offset = 1 if time.type == 'starting' else 2
            increment = offset if prev_time.type == 'ending' else 0
            points[time.value] = counter + increment
    prev_time = time

points_peak = max(points.values()) if points else 0
points = [(p, p) for p in points if points[p] == points_peak]
if points_peak > peak:
    peak = points_peak
    ranges = points
elif points_peak == peak:
    ranges += points

for stime, etime in sorted(ranges):
    print('%s-%s;%d' % (stime, etime, peak))
