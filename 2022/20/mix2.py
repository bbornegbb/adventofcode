#!/usr/bin/env python

import collections
from pprint import pprint

OFFSETS = 1000, 2000, 3000
DECRYPTION_KEY = 811589153
ROUNDS = 10

Item = collections.namedtuple("Item", "value has_moved is_last")


class Node(object):
    def __init__(self, value, next, prev):
        self.value = value
        self.next = next
        self.prev = prev

    def __repr__(self):
        return f"Node({self.value!r}, ...)"

    def move_after(self, other):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = other
        self.next = other.next
        other.next.prev = self
        other.next = self

    def move_before(self, other):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = other
        self.prev = other.prev
        other.prev.next = self
        other.prev = self


class LinkedList(Node):
    def __init__(self, iterable=None):
        super().__init__(None, self, self)
        self.length = 0
        if iterable != None:
            self.extend(iterable)

    def append(self, value):
        n = Node(value, self, self.prev)
        self.prev.next = n
        self.prev = n
        self.length += 1

    def appendleft(self, value):
        n = Node(value, self.next, self)
        self.next.prev = n
        self.next = n
        self.length += 1

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    def __repr__(self):
        return f'LinkedList([{", ".join(repr(n.value) for n in self.iternodes())}])'

    def __len__(self):
        return self.length

    def iternodes(self):
        next = self.next
        while next != self:
            yield next
            next = next.next

    def walk_right(self, node, amount):
        n = node
        for i in range(amount):
            n = n.next
            if n == self:
                n = n.next
        return n

    def walk_left(self, node, amount):
        n = node
        for i in range(amount):
            n = n.prev
            if n == self:
                n = n.prev
        return n

    def check(self):
        for n in self.iternodes():
            assert n.next.prev == n
            assert n.prev.next == n
        assert self.next.prev == self
        assert self.prev.next == self


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield int(line)


def mix(data):
    ll = LinkedList(data)
    nodes = list(ll.iternodes())
    l = len(nodes)
    for _ in range(ROUNDS):
        for node in nodes:
            amount = node.value % (l - 1)
            if node.value < 0 and amount > 0:
                amount -= l - 1
            if amount > 0:
                node.move_after(ll.walk_right(node, amount))
            elif amount < 0:
                node.move_before(ll.walk_left(node, -amount))
    return list(node.value for node in ll.iternodes())


def analyze(fname):
    data = list(DECRYPTION_KEY * v for v in read_data(fname))
    m = mix(data)
    l = len(m)
    idx = m.index(0)
    s = [(offs, m[(offs + idx) % l]) for offs in OFFSETS]
    return data, m, idx, l, s, sum(i[1] for i in s)


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
