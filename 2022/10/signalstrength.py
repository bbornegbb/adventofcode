#!/usr/bin/env python


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
    strength = 0
    for cycle, x in analyze_(fname):
        if (cycle - 20) % 40 == 0:
            # print(cycle, x)
            strength += cycle * x
    return strength


if __name__ == "__main__":
    # print(analyze("test.txt"))
    # print(analyze("test2.txt"))
    print(analyze("input.txt"))
