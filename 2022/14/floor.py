#!/usr/bin/env python

import collections
import itertools

import numpy as np

Point = collections.namedtuple("Point", "x, y")

EMPTY = 0
WALL = 1
SAND = 2
NOZZLE = 3

NOZZLE_LOC = Point(500, 0)


class Board(object):
    __slots__ = ("data", "xmin", "ymin")

    @staticmethod
    def from_scans(scans):
        xmin, xmax, ymin, ymax = minmax(scans)
        # sand starts falling at (500, 0) - align ymin with that
        ymin = min(ymin, NOZZLE_LOC.y)
        # bump ymax by two so we can add a floor
        ymax += 2
        # Add margins left and right to enable the floor. To be on the safe
        # side we need y to strech out in each direction by at least the nozzle
        # height from the nozzle location.
        nozzle_height = ymax - NOZZLE_LOC.y
        xmin = min(xmin, NOZZLE_LOC.x - nozzle_height)
        xmax = max(xmax, NOZZLE_LOC.x + nozzle_height)
        assert xmin <= NOZZLE_LOC.x <= xmax, ValueError(f"Sand falling outside board")
        print(xmin, xmax, ymin, ymax)
        b = Board()
        b.xmin = xmin
        b.ymin = ymin
        b.data = np.zeros((xmax - xmin + 1, ymax - ymin + 1), dtype="int8")
        b[NOZZLE_LOC] = NOZZLE
        b.data[:, ymax] = WALL
        for scan in scans:
            for p1, p2 in itertools.pairwise(scan):
                if p1.x == p2.x:
                    start, end = (p1.y, p2.y) if p2.y > p1.y else (p2.y, p1.y)
                    for y in range(start, end + 1):
                        b[p1.x, y] = WALL
                elif p1.y == p2.y:
                    start, end = (p1.x, p2.x) if p2.x > p1.x else (p2.x, p1.x)
                    for x in range(start, end + 1):
                        b[x, p1.y] = WALL
                else:
                    raise ValueError(f"Diagonal line: {p1} -> {p2}")
        return b

    def __getitem__(self, idx):
        assert isinstance(idx, tuple) and len(idx) == 2, KeyError("Only 2d access")
        x, y = idx
        return self.data[x - self.xmin, y - self.ymin]

    def __setitem__(self, idx, value):
        assert isinstance(idx, tuple) and len(idx) == 2, KeyError("Only 2d access")
        x, y = idx
        self.data[x - self.xmin, y - self.ymin] = value

    def __str__(self):
        return "\n".join("".join(int2field(v) for v in row) for row in self.data.T)

    def sandcorn(self):
        startpoint = x, y = NOZZLE_LOC.x - self.xmin, NOZZLE_LOC.y - self.ymin
        data = self.data
        xmax, ymax = data.shape
        xmax -= 1
        ymax -= 1
        while True:
            if data[x, y + 1] == EMPTY:
                y += 1
            elif data[x - 1, y + 1] == EMPTY:
                x -= 1
                y += 1
            elif data[x + 1, y + 1] == EMPTY:
                x += 1
                y += 1
            else:
                data[x, y] = SAND
                return (x, y) != startpoint


def int2field(i):
    if i == EMPTY:
        return "."
    elif i == WALL:
        return "#"
    elif i == SAND:
        return "o"
    elif i == NOZZLE:
        return "+"
    else:
        raise ValueError(f"Unknown field type: {i}")


def read_data(fname):
    with open(fname) as f:
        for line in f:
            points = line.strip().split(" -> ")
            yield [Point(*map(int, p.split(","))) for p in points]


def minmax(scans):
    return (
        min(point.x for scan in scans for point in scan),
        max(point.x for scan in scans for point in scan),
        min(point.y for scan in scans for point in scan),
        max(point.y for scan in scans for point in scan),
    )


def analyze(fname):
    scans = list(read_data(fname))
    board = Board.from_scans(scans)
    sandcorn = board.sandcorn
    for i in itertools.count():
        if not sandcorn():
            break
    print(i + 1)
    return board


if __name__ == "__main__":
    # print(analyze("test.txt"))
    analyze("input.txt")
