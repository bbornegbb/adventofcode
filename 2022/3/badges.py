#!/usr/bin/env python

import collections
import itertools

def priority(alpha):
    if 'a' <= alpha <= 'z':
        return ord(alpha) - ord('a') + 1
    elif 'A' <= alpha <= 'Z':
        return ord(alpha) - ord('A') + 27


def test_priority():
    for a in "abcxyzABCXYZ":
        print(a, priority(a))


def badge(h1, h2):
    c1 = collections.Counter(h1)
    c2 = collections.Counter(h2)
    shared = (c1 & c2).keys()
    return sum(priority(k) for k in shared)


def analyze(fname="input.txt"):
    total = 0
    def lines():
        with open(fname) as f:
            for line in f:
                yield line.strip()
    k = lines()
    try:
        while True:
            s1 = set(next(k))
            s2 = set(next(k))
            s3 = set(next(k))
            r = s1 & s2 & s3
            assert len(r) == 1
            total += priority(r.pop())
    except StopIteration:
        pass
    return total


if __name__ == "__main__":
    print(analyze())
