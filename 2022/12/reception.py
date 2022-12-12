#!/usr/bin/env python


import numpy as np
import networkx as nx


def read_data(fname):
    with open(fname) as f:
        return np.array([[ord(c) for c in line.strip()] for line in f], dtype=np.int16)


def compute_edges(data):
    X, Y = data.shape
    for x in range(X):
        for y in range(Y):
            xy = (x, y)
            x1y = (x + 1, y)
            xy1 = (x, y + 1)
            pairs = []
            if x + 1 < X:
                pairs.append((xy, x1y))
                pairs.append((x1y, xy))
            if y + 1 < Y:
                pairs.append((xy, xy1))
                pairs.append((xy1, xy))
            for l1, l2 in pairs:
                if data[l2] - data[l1] <= 1:
                    yield (l1, l2)


def where2tuple(a):
    assert (
        len(a[0]) == len(a[1]) == 1
    ), f"Need exactly 1 found location, found {len(a[0])} in {a}"
    return (a[0][0], a[1][0])


def analyze(fname):
    data = read_data(fname)
    source = where2tuple(np.where(data == ord("S")))
    target = where2tuple(np.where(data == ord("E")))
    data[source] = ord("a") - 1
    data[target] = ord("z")
    G = nx.DiGraph(compute_edges(data))
    return len(nx.shortest_path(G, source, target)) - 1


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
