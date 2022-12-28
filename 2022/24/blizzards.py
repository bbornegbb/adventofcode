#!/usr/bin/env python

import collections
import itertools

import numpy as np
import networkx as nx


MAX_ITER = 400


class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Blizzards(object):
    def __init__(self, direction, wrapx, wrapy, xy):
        self.dir = direction
        self.wrapx = wrapx
        self.wrapy = wrapy
        self.locations = np.array(xy)
        if direction == "^":
            self.move = self.up
        elif direction == "v":
            self.move = self.down
        elif direction == "<":
            self.move = self.left
        elif direction == ">":
            self.move = self.right
        else:
            raise ValueError("Unknown direction: {direction}")

    def up(self):
        y = self.locations[:, 1]
        y -= 1
        y[y == 0] = self.wrapy - 1

    def down(self):
        y = self.locations[:, 1]
        y += 1
        y[y == self.wrapy] = 1

    def left(self):
        x = self.locations[:, 0]
        x -= 1
        x[x == 0] = self.wrapx - 1

    def right(self):
        x = self.locations[:, 0]
        x += 1
        x[x == self.wrapx] = 1


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield line.strip()


def prepare_data(fname):
    data = read_data(fname)
    blizzards = {
        "^": [],
        "v": [],
        "<": [],
        ">": [],
    }
    for row, line in enumerate(data):
        if row == 0:
            start = (line.index("."), 0)
        for col, c in enumerate(line):
            if c in "<>^v":
                blizzards[c].append((col, row))
    end = (line.index("."), row)
    wrapx = col
    wrapy = row
    blizz = [
        Blizzards(d, wrapx, wrapy, xy) for d, xy in blizzards.items() if len(xy) > 0
    ]
    return start, end, len(line), row + 1, blizz


def generate_fields(xmax, ymax, start, end, blizzards):
    while True:
        field = np.full((xmax, ymax), ord("."), dtype=np.byte)
        field[0] = field[xmax - 1] = field[:, 0] = field[:, ymax - 1] = ord("#")
        field[start] = field[end] = ord(".")
        for b in blizzards:
            loc = b.locations
            field[loc[:, 0], loc[:, 1]] = ord(b.dir)
            b.move()
        yield field


def render_field(field):
    return "\n".join("".join(chr(c) for c in row) for row in field.T)


def node_name(time, x, y):
    return f"t={time} x={x} y={y}"


def analyze(fname):
    start, end, xmax, ymax, blizzards = prepare_data(fname)
    print("Build graph")
    G = nx.DiGraph()
    for iteration, (f1, f2) in enumerate(
        itertools.pairwise(generate_fields(xmax, ymax, start, end, blizzards))
    ):
        locs = np.where(f1 == ord("."))
        for x, y in zip(*locs):
            snode = node_name(iteration, x, y)
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                x2 = x + dx
                y2 = y + dy
                if x2 < 0 or y2 < 0 or x2 >= xmax or y2 >= ymax:
                    continue
                if f2[x2, y2] == ord("."):
                    enode = node_name(iteration + 1, x2, y2)
                    G.add_edge(snode, enode)
        if iteration == MAX_ITER:
            break
    print("Start Dijkstra")
    paths = nx.shortest_paths.single_source_dijkstra_path(G, node_name(0, *start))
    for i in range(MAX_ITER + 1):
        name = node_name(i, *end)
        if name in paths:
            return i, paths[name], start, end
    return -1, [], start, end


if __name__ == "__main__":
    # print(analyze("test.txt"))
    # print(analyze("test2.txt"))
    # print(analyze("test3.txt"))
    print(analyze("input.txt"))
