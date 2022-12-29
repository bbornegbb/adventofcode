#!/usr/bin/env python

import collections

from pprint import pprint

import numpy as np


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield line.rstrip("\n")


def prep_data(data):
    lines = list(data)
    passcode = lines.pop()
    empty = lines.pop()
    assert empty == "", "File format not recognized"
    width = max(len(l) for l in lines)
    height = len(lines)
    field = np.full((width, height), ord(" "), dtype=np.uint8)
    for i, l in enumerate(lines):
        field[: len(l), i] = [ord(c) for c in l]
    xminmax = []
    yminmax = []
    for i in range(field.shape[1]):
        valid = np.where(field[:, i] != ord(" "))[0]
        assert valid[-1] - valid[0] + 1 == len(valid), "Found hole in playing field"
        xminmax.append((valid[0], valid[-1]))
    for i in range(field.shape[0]):
        valid = np.where(field[i, :] != ord(" "))[0]
        assert valid[-1] - valid[0] + 1 == len(valid), "Found hole in playing field"
        yminmax.append((valid[0], valid[-1]))
    return field, passcode, xminmax, yminmax


def render_field(field):
    return "\n".join("".join(chr(c) for c in row) for row in field.T)


# direction[0] is the current direction. Moving forward through the dec
# corresponds to rotating right, moving backwards to rotating left. Starting
# position is right facing.
def make_directions():
    return collections.deque([">", "v", "<", "^"])


def dir_value(direction):
    dirs = make_directions()
    return dirs.index(direction)


def parse(passcode):
    buf = ""
    for c in passcode:
        if c in "RL":
            if buf != "":
                yield int(buf)
                buf = ""
            yield c
        else:
            buf += c
    if buf != "":
        yield int(buf)


def compute_pos(old, direction, xminmax, yminmax):
    nx, ny = old
    if direction == "^":
        min_, max_ = yminmax[nx]
        ny -= 1
        if ny < min_:
            ny = max_
    elif direction == "v":
        min_, max_ = yminmax[nx]
        ny += 1
        if ny > max_:
            ny = min_
    elif direction == "<":
        min_, max_ = xminmax[ny]
        nx -= 1
        if nx < min_:
            nx = max_
    else:  # diretion == '>'
        min_, max_ = xminmax[ny]
        nx += 1
        if nx > max_:
            nx = min_
    return nx, ny


def analyze(fname):
    data = read_data(fname)
    field, passcode, xminmax, yminmax = prep_data(data)
    xstart = np.min(np.where(field[:, 0] == ord(".")))
    pos = xstart, 0
    dirs = make_directions()
    field[pos] = ord(dirs[0])
    # print(render_field(field))
    for instruction in parse(passcode):
        # print("Instruction:", instruction)
        if instruction == "L":
            dirs.rotate(1)
            field[pos] = ord(dirs[0])
        elif instruction == "R":
            dirs.rotate(-1)
            field[pos] = ord(dirs[0])
        else:  # integer, move forward by specified amount
            d = dirs[0]
            for _ in range(instruction):
                newpos = compute_pos(pos, d, xminmax, yminmax)
                if field[newpos] == ord("#"):
                    break
                pos = newpos
                field[pos] = ord(dirs[0])
        # print(render_field(field))
    col = pos[0] + 1
    row = pos[1] + 1
    dv = dir_value(dirs[0])
    # print(render_field(field))
    return f"row={row}  col={col}  dir_value={dv}  password={1000 * row + 4 * col + dv}"


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
