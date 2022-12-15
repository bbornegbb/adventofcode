#!/usr/bin/env python

import collections
import re

# Example: "Sensor at x=9, y=16: closest beacon is at x=10, y=16"
LINE_PATTERN = (
    r"Sensor at x=(?P<x>-?\d+), y=(?P<y>-?\d+): "
    r"closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)"
)


Point = collections.namedtuple("Point", "x y")
Sensor = collections.namedtuple("Sensor", "loc beacon")
Range = collections.namedtuple("Range", "start end")


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


def merge_ranges(ranges):
    ranges = sorted(ranges)
    start, end = ranges[0]
    for r in ranges[1:]:
        if r.start <= end + 1:
            end = max(end, r.end)
        else:
            rv = Range(start, end)
            start = r.start
            end = r.end
            yield rv
    yield Range(start, end)


def gap(ranges, max_):
    if len(ranges) == 2:
        assert ranges[0].end + 2 == ranges[1].start, ValueError(
            f"Gap is too large for {ranges}"
        )
        return ranges[0].end + 1
    else:
        assert len(ranges) == 1, ValueError(f"Need exactly 1 or 2 ranges, got {ranges}")
        r = ranges[0]
        if r.start == 1:
            return 0
        elif r.end == max_ - 1:
            return max_
        else:
            raise ValueError(f"Range {range} does not have a unique gap in (0, {max_})")


def analyze(fname, max_):
    data = list(read_data(fname))
    for target_y in range(max_ + 1, -1, -1):
        if target_y % 100000 == 0:
            print("Progress:", target_y)
        ranges = []
        for s in data:
            d = manhatten(s.loc, s.beacon)
            vd = abs(s.loc.y - target_y)
            n = d - vd
            if n >= 0:
                xmin = max(s.loc.x - n, 0)
                xmax = min(s.loc.x + n, max_)
                ranges.append(Range(xmin, xmax))
        ranges = list(merge_ranges(ranges))
        isfull = len(ranges) == 1 and ranges[0] == Range(0, max_)
        if not isfull:
            x = gap(ranges, max_)
            return f"x={x}  y={target_y}  tuning={4000000 * x + target_y}"


if __name__ == "__main__":
    # print(analyze("test.txt", 20))
    print(analyze("input.txt", 4000000))
