#!/usr/bin/env python

import collections
import re

# Sensor at x=9, y=16: closest beacon is at x=10, y=16
LINE_PATTERN = (
    r"Sensor at x=(?P<x>-?\d+), y=(?P<y>-?\d+): "
    r"closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)"
)


Point = collections.namedtuple("Point", "x y")
Sensor = collections.namedtuple("Sensor", "loc beacon")


def read_data(fname):
    r = re.compile(LINE_PATTERN)
    with open(fname) as f:
        for line in f:
            match = r.match(line)
            gd = match.groupdict()
            s = Point(int(gd["x"]), int(gd["y"]))
            b = Point(int(gd["bx"]), int(gd["by"]))
            yield Sensor(s, b)


def manhatten(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def analyze(fname, target_y):
    data = read_data(fname)
    excluded = set()
    beacons = set()
    for s in data:
        d = manhatten(s.loc, s.beacon)
        if s.beacon.y == target_y:
            beacons.add(s.beacon.x)
        vd = abs(s.loc.y - target_y)
        n = d - vd
        if n >= 0:
            excluded.update(range(s.loc.x - n, s.loc.x + n + 1))
    return len(excluded), len(beacons), len(excluded - beacons)


if __name__ == "__main__":
    # print(analyze("test.txt", 10))
    print(analyze("input.txt", 2000000))
