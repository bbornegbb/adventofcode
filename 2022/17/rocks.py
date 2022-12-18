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


def print_cave(cave, height):
    for h in range(height, -1, -1):
        row = cave[:, h]
        print("".join("#" if item else "." for item in row))


def analyze(fname, rock_cnt=2022):
    data = read_data(fname).strip()
    rocksdata = read_data("rocks.txt")
    rockshapes = [parse_rock(rd) for rd in rocksdata.split("\n\n")]
    agg_rocks_height = sum(r.shape[1] for r in rockshapes)
    max_tower_height = (rock_cnt + 2) * agg_rocks_height // len(rockshapes) + 3
    cave = np.zeros((WIDTH, max_tower_height), dtype="int8")
    height = 0
    rocks_iter = itertools.cycle(rockshapes)
    jets = itertools.cycle(data)
    for cnt in range(rock_cnt):
        rock = next(rocks_iter)
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
                break
    return height


if __name__ == "__main__":
    # pprint(analyze("test.txt"))
    pprint(analyze("input.txt"))
