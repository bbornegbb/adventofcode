#!/usr/bin/env python

import bisect


def insert_if_larger(l, value):
    if value > l[0]:
        bisect.insort(l, value)
        return l[1:]
    else:
        return l


def analyze(filename="input.txt"):
    calories = 0
    maxcalories = [0, 0, 0]
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "":
                maxcalories = insert_if_larger(maxcalories, calories)
                calories = 0
            else:
                calories += int(line)
    return insert_if_larger(maxcalories, calories)


if __name__ == "__main__":
    print(sum(analyze()))
