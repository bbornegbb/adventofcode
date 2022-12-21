#!/usr/bin/env python

# Could be further optimized by memoizing has_human() and get_value()
# but runs in 0.05s as is already.

import collections
import operator


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield line.strip().split()


class LeafMonkey(collections.namedtuple("LeafMonkey_", "name value md")):
    def get_value(self):
        return self.value

    def has_human(self):
        return self.name == HUMAN


class OpMonkey(collections.namedtuple("OpMonkey_", "name lmonkey op rmonkey md")):
    def get_value(self):
        return self.op(
            self.md[self.lmonkey].get_value(), self.md[self.rmonkey].get_value()
        )

    def has_human(self):
        return (
            self.name == HUMAN
            or self.md[self.lmonkey].has_human()
            or self.md[self.rmonkey].has_human()
        )

    def left(self):
        return self.md[self.lmonkey]

    def right(self):
        return self.md[self.rmonkey]


HUMAN = "humn"

ops = {
    "*": operator.mul,
    "/": operator.floordiv,
    "-": operator.sub,
    "+": operator.add,
    "=": operator.eq,
}


def search(root, target):
    if root.name == HUMAN:
        return target
    rl = root.left()
    if rl.has_human():
        newroot = rl
        value = root.right().get_value()
        if root.op == operator.mul:
            tgt = target // value
        elif root.op == operator.floordiv:
            tgt = target * value
        elif root.op == operator.add:
            tgt = target - value
        else:  # root.op == operator.sub
            tgt = target + value
    else:  # root.right().has_human()
        assert root.right().has_human()
        newroot = root.right()
        value = root.left().get_value()
        if root.op == operator.mul:
            tgt = target // value
        elif root.op == operator.floordiv:
            tgt = value // target
        elif root.op == operator.add:
            tgt = target - value
        else:  # root.op == operator.sub:
            tgt = value - target
    return search(newroot, tgt)


def analyze(fname):
    data = read_data(fname)
    monkeys = dict()
    for tokens in data:
        name = tokens[0].strip(":")
        if len(tokens) == 2:
            monkeys[name] = LeafMonkey(name, int(tokens[1]), monkeys)
        elif len(tokens) == 4:
            if name == "root":
                op = ops["="]
            else:
                op = ops[tokens[2]]
            monkeys[name] = OpMonkey(name, tokens[1], op, tokens[3], monkeys)
        else:
            raise ValueError("Cannot parse file")

    root = monkeys["root"]
    assert root.has_human(), "Graph should have a human but not found"
    if root.left().has_human():
        valueroot = root.right()
        target = valueroot.get_value()
        searchroot = root.left()
    else:
        valueroot = root.left()
        target = valueroot.get_value()
        searchroot = root.right()

    v = search(searchroot, target)

    monkeys[HUMAN] = LeafMonkey(HUMAN, v, monkeys)
    got = searchroot.get_value()
    assert got == target, "Want: {target}  got: {v2}  injected: {v}"
    return v


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
