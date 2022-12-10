#!/usr/bin/env python

import itertools


def get_input(fname):
    with open(fname) as f:
        return f.read().strip()


def analyze(fname):
    input = get_input(fname)
    for i in range(0, len(input) - 14):
        candidate = input[i : i + 14]
        if len(set(candidate)) == 14:
            return i + 14
    return -1


if __name__ == "__main__":
    print(analyze("input.txt"))
