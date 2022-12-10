#!/usr/bin/env python

import itertools


def get_input(fname):
    with open(fname) as f:
        return f.read().strip()


def analyze(fname):
    input = get_input(fname)
    a, b, c, d = itertools.tee(input, 4)
    next(b)
    next(c)
    next(c)
    next(d)
    next(d)
    next(d)
    for i, fourtuple in enumerate(zip(a, b, c, d)):
        if len(set(fourtuple)) == 4:
            return i + 4
    return -1


if __name__ == "__main__":
    print(analyze("input.txt"))
