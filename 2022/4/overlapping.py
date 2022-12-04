#!/usr/bin/env python

class Elve(object):
    def __init__(self, sections):
        self.start, self.end = (int(s) for s in sections.split("-"))


    def contains(self, other):
        return self.start <= other.start and self.end >= other.end


    def overlaps(self, other):
        return ((self.start <= other.start and self.end >= other.start) or
                 (other.start <= self.start and other.end >= self.start))


    def __str__(self):
        return f"Elve('{self.start}-{self.end}')"


def parse_line(line):
    elv1, elv2 = line.strip().split(",")
    return Elve(elv1), Elve(elv2)


def analyze(fname="input.txt"):
    count = 0
    with open(fname) as f:
        for line in f:
            e1, e2 = parse_line(line)
            if e1.overlaps(e2):
                # print(f"{e1} overlaps {e2}")
                count += 1
            # else:
            #     print(f"{e1} does not overlap {e2}")
    return count


if __name__ == "__main__":
    print(analyze())
