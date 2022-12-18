#!/usr/bin/env python


import numpy as np

OFFSETS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield tuple(int(i) for i in line.strip().split(","))


def surface(a, rock):
    sf = 0
    for x, y, z in a:
        for ox, oy, oz in OFFSETS:
            if rock[x + ox, y + oy, z + oz] == 0:
                sf += 1
    return sf


def outside(rock, o_in=None):
    s = rock.shape
    if o_in is None:
        o = np.zeros(s, rock.dtype)
    else:
        o = o_in.copy()
    # from construction, we know that there is never rock at any
    # 0 or maximum coordinate
    o[0, :, :] = 1
    o[:, 0, :] = 1
    o[:, :, 0] = 1
    o[s[0] - 1, :, :] = 1
    o[:, s[1] - 1, :] = 1
    o[:, :, s[2] - 1] = 1
    for x in range(1, s[0] - 1):
        for y in range(1, s[1] - 1):
            for z in range(1, s[2] - 1):
                if rock[x, y, z] == 1:
                    continue
                for ox, oy, oz in OFFSETS:
                    if o[x + ox, y + oy, z + oz] == 1:
                        o[x, y, z] = 1
                        break
    if o_in is None or np.any(o != o_in):
        return outside(rock, o)
    else:
        return o


def analyze(fname):
    # bumping coordinates so to avoid annoying
    # boundary checks in surface and outside computations
    data = list([x + 1, y + 1, z + 1] for x, y, z in read_data(fname))
    a = np.array(data, dtype="int8")
    shape = tuple(i + 2 for i in np.max(a, axis=0))
    rock = np.zeros(shape, dtype="int8")
    for x, y, z in a:
        rock[x, y, z] = 1
    o = outside(rock)
    filled_rock = 1 - o
    return surface(a, filled_rock)


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
