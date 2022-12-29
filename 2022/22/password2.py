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


def compute_pos(old, direction, wrapping):
    nx, ny = old
    if direction == "^":
        ny -= 1
    elif direction == "v":
        ny += 1
    elif direction == "<":
        nx -= 1
    else:  # diretion == '>'
        nx += 1
    new = (nx, ny)
    try:
        return wrapping[(nx, ny)]
    except KeyError:
        return new, ""


def wrapping_rules_test_txt(shape):
    xmax, ymax = shape
    rv = {}
    # Top 4 rows, fore and back paths
    for i in range(4):
        rv[(7, i)] = (4 + i, 4), "L"
        rv[(4 + i, 3)] = (8, i), "R"
        rv[(12, i)] = (xmax - 1, ymax - i - 1), "RR"
        rv[(xmax, ymax - i - 1)] = (11, i), "LL"
    # Middle 4 rows, fore and back paths
    for i in range(4, 8):
        rv[(-1, i)] = (xmax - i + 3, ymax - 1), "R"
        rv[(xmax - i + 3, ymax)] = (0, i), "L"
        rv[(12, i)] = (xmax - i + 3, 8), "R"
        rv[(xmax - i + 3, 7)] = (11, i), "L"
    # Lower 4 rows, fore and back paths; right side already connected
    for i in range(8, 12):
        rv[(7, i)] = (xmax - i - 1, 7), "R"
        rv[(xmax - i, 7)] = (8, i), "L"
    # Remaining column links, fore and back paths
    for i in range(8, 12):
        rv[(i, -1)] = (11 - i, 4), "LL"
        rv[(11 - i, 3)] = (i, 0), "RR"
        rv[(i, 12)] = (11 - i, 7), "RR"
        rv[(11 - i, 8)] = (i, 11), "LL"
    return rv


def wrapping_rules_input_txt(shape):
    xmax, ymax = shape
    rv = {}
    # Top 50 lines
    l_out = 49
    l_in = 50
    r_out = 150
    r_in = 149
    for i in range(50):
        rv[(l_out, i)] = (0, 149 - i), "RR"
        rv[(-1, 149 - i)] = (l_in, i), "LL"
        rv[(r_out, i)] = (99, 149 - i), "LL"
        rv[(100, 149 - i)] = (r_in, i), "RR"
    # Next 50 lines
    l_out = 49
    l_in = 50
    r_out = 100
    r_in = 99
    for i in range(50, 100):
        rv[(l_out, i)] = (i - 50, 100), "L"
        rv[(i - 50, 99)] = (l_in, i), "R"
        rv[(r_out, i)] = (i + 50, 49), "L"
        rv[(i + 50, 50)] = (r_in, i), "R"

    # Third 50 lines connected to first 50 lines

    # Last 50 lines
    l_out = -1
    l_in = 0
    r_out = 50
    r_in = 49
    for i in range(150, 200):
        rv[(l_out, i)] = (i - 100, 0), "L"
        rv[(i - 100, -1)] = (l_in, i), "R"
        rv[(r_out, i)] = (i - 100, 149), "L"
        rv[(i - 100, 150)] = (r_in, i), "R"

    # Direct bottom-top connections
    b_out = 200
    b_in = 199
    t_out = -1
    t_in = 0
    for i in range(50):
        rv[(i, b_out)] = (i + 100, t_in), ""
        rv[(i + 100, t_out)] = (i, b_in), ""

    return rv


# TODO: We should compute these algorithmically instead
# of hardcoding
def wrapping_rules(fname, shape, xminmax, yminmax):
    # test.txt
    if fname == "test.txt":
        return wrapping_rules_test_txt(shape)
    elif fname == "input.txt":
        return wrapping_rules_input_txt(shape)
    else:
        raise ValueError(f"Generic input files not supported yet: {fname!r}")


def analyze(fname):
    data = read_data(fname)
    field, passcode, xminmax, yminmax = prep_data(data)
    wrapping = wrapping_rules(fname, field.shape, xminmax, yminmax)
    # print(sorted(wrapping.items()))
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
            for _ in range(instruction):
                d = dirs[0]
                newpos, rotate = compute_pos(pos, d, wrapping)
                # print(newpos, rotate)
                if field[newpos] == ord("#"):
                    break
                assert (
                    chr(field[newpos]) in ".<>^v"
                ), f"Warped to nirvana: {pos} {d} {newpos} {rotate}"
                pos = newpos
                for r in rotate:
                    if r == "L":
                        dirs.rotate(1)
                    else:
                        dirs.rotate(-1)
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
