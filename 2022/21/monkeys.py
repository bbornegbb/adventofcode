#!/usr/bin/env python

import collections
import operator


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield line.strip().split()


class LeafMonkey(collections.namedtuple("LeafMonkey_", "name value")):
    def get_value(self, md):
        return self.value


class OpMonkey(collections.namedtuple("OpMonkey_", "name lmonkey op rmonkey")):
    def get_value(self, md):
        return self.op(md[self.lmonkey].get_value(md), md[self.rmonkey].get_value(md))


ops = {
    "*": operator.mul,
    "/": operator.floordiv,
    "-": operator.sub,
    "+": operator.add,
}


def analyze(fname):
    data = read_data(fname)
    monkeys = dict()
    for tokens in data:
        name = tokens[0].strip(":")
        if len(tokens) == 2:
            monkeys[name] = LeafMonkey(name, int(tokens[1]))
        elif len(tokens) == 4:
            monkeys[name] = OpMonkey(name, tokens[1], ops[tokens[2]], tokens[3])
        else:
            raise ValueError("Cannot parse file")
    return monkeys, monkeys["root"].get_value(monkeys)


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
