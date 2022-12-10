#!/usr/bin/env python

import numpy as np

def read_data(fname):
    with open(fname) as f:
        for line in f:
            if line.startswith("noop"):
                yield "noop", 0
            else:
                o, a = line.split()
                yield o, int(a)


def analyze_(fname):
    data = read_data(fname)
    x = 1
    cycle = 1
    for op, amount in data:
        if op == "noop":
            yield cycle, x
            cycle += 1
        else:
            yield cycle, x
            yield cycle + 1, x
            cycle += 2
            x += amount
    yield cycle, x

def analyze(fname):
    screen = np.zeros((6, 40), bool)
    for clock, (cycle, x) in enumerate(analyze_(fname)):
        ncol = clock % 40
        if ncol - 1 <= x <= ncol + 1:
            nrow = (clock // 40) % 6
            screen[nrow, ncol] = True
    return "\n".join("".join('#' if b else ' ' for b in row) for row in screen)


if __name__ == "__main__":
    #print(analyze("test.txt"))
    #print(analyze("test2.txt"))
    print(analyze("input.txt"))

