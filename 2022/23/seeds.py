#!/usr/bin/env python

import collections
import itertools

Elf = collections.namedtuple("Elf", "x y")

DIR_N = (0, -1)
DIR_NE = (1, -1)
DIR_E = (1, 0)
DIR_SE = (1, 1)
DIR_S = (0, 1)
DIR_SW = (-1, 1)
DIR_W = (-1, 0)
DIR_NW = (-1, -1)

ALL_DIR = [DIR_N, DIR_NE, DIR_E, DIR_SE, DIR_S, DIR_SW, DIR_W, DIR_NW]

NORTH = [DIR_NW, DIR_N, DIR_NE]
SOUTH = [DIR_SW, DIR_S, DIR_SE]
EAST = [DIR_NE, DIR_E, DIR_SE]
WEST = [DIR_SW, DIR_W, DIR_NW]


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield line.strip()


def prepare_data(fname):
    data = read_data(fname)
    elves = set()
    for row, line in enumerate(data):
        for col, c in enumerate(line):
            if c == "#":
                elves.add(Elf(col, row))
    return elves


def minmax(iterable):
    min_ = max_ = None
    for v in iterable:
        if min_ is None or v < min_:
            min_ = v
        if max_ is None or v > max_:
            max_ = v
    return min_, max_


def draw_field(elves):
    xmin, xmax = minmax(e.x for e in elves)
    dx = xmax - xmin + 1
    s = sorted(elves, key=lambda e: (e.y, e.x))
    k_old = s[0].y
    rv = [f"Origin ({xmin}, {k_old})"]
    for k, g in itertools.groupby(s, key=lambda e: e.y):
        for _ in range(k_old + 1, k):
            rv.append("." * dx)
        k_old = k
        l = ["."] * dx
        for e in g:
            l[e.x - xmin] = "#"
        rv.append("".join(l))
    return "\n".join(rv)


def move(elves, checks):
    def move_one(elf):
        if not any(Elf(elf.x + dx, elf.y + dy) in elves for dx, dy in ALL_DIR):
            return elf, elf
        for check, d in checks:
            if not any(Elf(elf.x + dx, elf.y + dy) in elves for dx, dy in check):
                return elf, Elf(elf.x + d[0], elf.y + d[1])
        return elf, elf

    proposed_moves = [move_one(elf) for elf in elves]
    new_positions = collections.Counter(new for _, new in proposed_moves)
    blocked = set(pos for pos, cnt in new_positions.items() if cnt > 1)
    return set(old if new in blocked else new for old, new in proposed_moves)


def analyze(fname):
    elves = prepare_data(fname)
    checks = collections.deque(
        [
            (NORTH, DIR_N),
            (SOUTH, DIR_S),
            (WEST, DIR_W),
            (EAST, DIR_E),
        ]
    )
    for round in itertools.count(1):
        elves_new = move(elves, checks)
        if elves_new == elves:
            break
        checks.rotate(-1)
        elves = elves_new
        if round == 10:
            xmin, xmax = minmax(e.x for e in elves)
            ymin, ymax = minmax(e.y for e in elves)
            dx = xmax - xmin + 1
            dy = ymax - ymin + 1
    return (
        f"dx={dx}  dy={dy}  len(elves)={len(elves)}  "
        f"empty_fields={dx * dy - len(elves)}  round={round}"
    )


if __name__ == "__main__":
    # print(analyze("test.txt"))
    # print(analyze("test2.txt"))
    print(analyze("input.txt"))
