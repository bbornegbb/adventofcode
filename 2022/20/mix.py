#!/usr/bin/env python

import collections
from pprint import pprint

OFFSETS = 1000, 2000, 3000


Item = collections.namedtuple("Item", "value has_moved is_last")


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield int(line)


def mix(data):
    d = collections.deque(Item(v, False, False) for v in data)
    d.append(Item(d.pop().value, False, True))
    l = len(d)
    while True:
        e = d.popleft()
        if e.has_moved:
            d.append(e)
        else:
            amount = e.value % (l - 1)
            if e.value < 0 and amount > 0:
                amount -= l - 1
            d.rotate(-amount)
            d.appendleft(Item(e.value, True, e.is_last))
            d.rotate(amount - (1 if amount <= 0 else 0))
        if e.is_last:
            d.rotate(-1)
            break
    return list(item.value for item in d)


def analyze(fname):
    data = list(read_data(fname))
    m = mix(data)
    l = len(m)
    idx = m.index(0)
    s = [(offs, m[(offs + idx) % l]) for offs in OFFSETS]
    return data, m, idx, l, s, sum(i[1] for i in s)


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
