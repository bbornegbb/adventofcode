#!/usr/bin/env python

import collections


def priority(alpha):
    if "a" <= alpha <= "z":
        return ord(alpha) - ord("a") + 1
    elif "A" <= alpha <= "Z":
        return ord(alpha) - ord("A") + 27


def test():
    for a in "abcxyzABCXYZ":
        print(a, priority(a))


def compare(h1, h2):
    c1 = collections.Counter(h1)
    c2 = collections.Counter(h2)
    shared = (c1 & c2).keys()
    return sum(priority(k) for k in shared)


def analyze(fname="input.txt"):
    total = 0
    with open(fname) as f:
        for line in f:
            line = line.strip()
            l = len(line)
            total += compare(line[: l // 2], line[l // 2 :])
    return total


if __name__ == "__main__":
    print(analyze())
