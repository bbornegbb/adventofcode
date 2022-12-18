#!/usr/bin/env python

import collections
import itertools

from pprint import pprint

import numpy as np

WIDTH = 7


Point = collections.namedtuple("Point", "x y")


def parse_rock(shape):
    rock = [[0 if c == "." else 1 for c in line] for line in shape.split("\n")[::-1]]
    return np.array(rock, dtype="int8").T


def read_data(fname):
    with open(fname) as f:
        return f.read().strip()


def try_move(cave, rockshape, pos, xamount, yamount):
    rocksize = rockshape.shape
    pl = Point(pos.x + xamount, pos.y + yamount)
    region = cave[pl.x : (pl.x + rocksize[0]), pl.y : (pl.y + rocksize[1])]
    if np.any((rockshape + region) == 2):
        return False, pos
    else:
        return True, pl


def try_fall(cave, rockshape, pos):
    if pos.y == 0:
        return False, pos
    return try_move(cave, rockshape, pos, 0, -1)


def try_move_left(cave, rockshape, pos):
    if pos.x == 0:
        return pos
    return try_move(cave, rockshape, pos, -1, 0)[1]


def try_move_right(cave, rockshape, pos):
    if pos.x + rockshape.shape[0] == WIDTH:
        return pos
    return try_move(cave, rockshape, pos, +1, 0)[1]


def print_cave(cave, height=None, bottom=-1):
    if height is None:
        height = cave.shape[1] - 1
    for h in range(height, bottom, -1):
        row = cave[:, h]
        print("".join("#" if item else "_" for item in row))


def analyze_one(fname, rock_cnt=2022):
    data = read_data(fname).strip()
    rocksdata = read_data("rocks.txt")
    rockshapes = [parse_rock(rd) for rd in rocksdata.split("\n\n")]
    agg_rocks_height = sum(r.shape[1] for r in rockshapes)
    max_tower_height = (rock_cnt + 2) * agg_rocks_height // len(rockshapes) + 3
    cave = np.zeros((WIDTH, max_tower_height), dtype="int8")
    height = 0
    rocks = itertools.cycle(rockshapes)
    jets = itertools.cycle(data)
    offset = 0
    recorded_heights = []
    for cnt in range(rock_cnt):
        rock = next(rocks)
        pos = Point(2, height + 3)
        while True:
            jet = next(jets)
            if jet == "<":
                pos = try_move_left(cave, rock, pos)
            elif jet == ">":
                pos = try_move_right(cave, rock, pos)
            else:
                raise ValueError(f"Invalid jet stream: {jet}")
            could_fall, pos = try_fall(cave, rock, pos)
            if not could_fall:
                cave[
                    pos.x : (pos.x + rock.shape[0]), pos.y : (pos.y + rock.shape[1])
                ] += rock
                height = max(height, pos.y + rock.shape[1])
                recorded_heights.append((height, cnt))
                break
    return cave, height, recorded_heights


def gcd(n1, n2):
    def gcd_(n1, n2):
        if n1 == 0:
            return n2
        return gcd_(n2 % n1, n1)

    return gcd_(min(n1, n2), max(n1, n2))


def find_pattern(cave, height, pattern):
    pheight = pattern.shape[1]
    for y in range(0, height - pheight):
        if np.all(cave[:, y : (y + pheight)] == pattern):
            yield y


def find_seasonality_user(height_cnt):
    from matplotlib import pyplot as plt

    diff = np.diff(height_cnt[:, 0])
    autocorrelation = np.array(
        [np.correlate(diff, np.roll(diff, k))[0] for k in range(np.alen(diff) // 2)]
    )
    plt.plot(autocorrelation)
    plt.show()
    print("Please provide seasonality estimate")
    seasonality = input()
    return int(seasonality)


def find_seasonality(cave, height_count, pattern_height=10):
    h = height_count[-1][0]
    h2 = h // 2
    pattern = cave[:, h2 : h2 + pattern_height]
    for y in range(h2 + 1, h - pattern_height):
        if np.all(cave[:, y : y + pattern_height] == pattern):
            break
    hd = y - h2
    if np.any(cave[:, h2 : y] != cave[:, h2 + hd : h2 + 2 * hd]):
        raise ValueError("Choose different parameters, finding repeating pattern failed")
    # hd now has the seasonality in tower height. We need to return
    # seasonality in number of rocks dropped, though.
    lhc = len(height_count)
    lhc2 = lhc // 2
    locs = np.where(height_count[lhc2:, 0] % hd == 0)
    seasonality = np.unique(np.diff(locs))
    if len(seasonality) != 1:
        raise ValueError(f"Choose different parameters, found multiple seasonalities: "
                         f"{seasonality}")
    return seasonality[0]


def analyze(fname, iterations, seasonality=None, correct_answer=None):
    target = 1000000000000

    cave, height, recorded_heights = analyze_one(fname, iterations)
    rh = np.array(recorded_heights, dtype="int64")

    if seasonality is None:
        try:
            seasonality = find_seasonality(cave, rh)
        except ValueError as e:
            # Fall back to the user in case we couldn't automatically find seasonality.
            print(e)
            seasonality = find_seasonality_user(rh)


    offset = 5 * seasonality
    tm = (target - offset) % seasonality
    offset += tm
    assert (target - offset) % seasonality == 0, "LogicError in offset computation"
    mul = (target - offset) // seasonality

    h0 = rh[offset - 1, 0]
    dh = rh[offset + seasonality, 0] - rh[offset, 0]
    answer = mul * dh + h0
    if correct_answer != None:
        assert answer == correct_answer, "LogicError in answer computation"
    return answer


if __name__ == "__main__":
    # pprint(analyze("test.txt", 500, None, 1514285714288))
    pprint(analyze("input.txt", 12000, None, 1570930232582))
    # pprint(analyze("input.txt", 20000, 1720, 1570930232582))
