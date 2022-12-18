#!/usr/bin/env python


import numpy as np

OFFSETS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield tuple(int(i) for i in line.strip().split(","))


def analyze(fname):
    data = list(read_data(fname))
    a = np.array(data, dtype="int8")
    shape = tuple(i + 2 for i in np.max(a, axis=0))
    rock = np.zeros(shape, dtype="int8")
    for x, y, z in a:
        rock[x, y, z] = 1
    surface = 0
    for x, y, z in a:
        for ox, oy, oz in OFFSETS:
            if rock[x + ox, y + oy, z + oz] == 0:
                surface += 1
    return a, shape, rock, surface


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
