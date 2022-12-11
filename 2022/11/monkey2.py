#!/usr/bin/env python


import math
import re

MONKEY_RE = (
    r"Monkey (?P<id>\d+):\n"
    r"  Starting items: (?P<items>[0-9, ]+)\n"
    r"  Operation: new = old (?P<op>[+*]) (?P<amount>(\d+|old)+)\n"
    r"  Test: divisible by (?P<divisible_by>\d+)\n"
    r"    If true: throw to monkey (?P<true_monkey_id>\d+)\n"
    r"    If false: throw to monkey (?P<false_monkey_id>\d+)"
)

monkey_re = re.compile(MONKEY_RE)


class Monkey(object):
    def __init__(self, id_, items, op, amount, divisible_by, true_monkey, false_monkey):
        self.id = id_
        self.items = items
        self.op = op
        self.amount = amount
        self.divisible_by = divisible_by
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspect_count = 0

    def __repr__(self):
        return (
            f"Monkey({self.id}, {self.items}, {self.op!r}, "
            f"{self.amount!r}, {self.divisible_by}, "
            f"{self.true_monkey}, {self.false_monkey})"
        )

    @classmethod
    def from_file(cls, f):
        lines = []
        for _, line in zip(range(6), f):
            lines.append(line)
        monkey_txt = "".join(lines)
        match = monkey_re.match(monkey_txt)
        if match is None:
            raise ValueError(f"Monkey parse error:\n{monkey_txt}")
        gd = match.groupdict()
        return cls(
            gd["id"],
            [int(i) for i in gd["items"].split(", ")],
            gd["op"],
            gd["amount"],
            int(gd["divisible_by"]),
            int(gd["true_monkey_id"]),
            int(gd["false_monkey_id"]),
        )

    def throw_to(self, monkeys, modulo):
        if self.op == "*":
            inspect_op = lambda x, y: x * y
        elif self.op == "+":
            inspect_op = lambda x, y: x + y
        for item in self.items:
            self.inspect_count += 1
            a = item if self.amount == "old" else int(self.amount)
            level = inspect_op(item, a)
            level %= modulo
            if level % self.divisible_by == 0:
                monkeys[self.true_monkey].catch(level)
            else:
                monkeys[self.false_monkey].catch(level)
        self.items = []

    def catch(self, level):
        self.items.append(level)


def read_data(fname):
    monkeys = []
    with open(fname) as f:
        while True:
            monkeys.append(Monkey.from_file(f))
            if f.readline() == "":
                break
    return monkeys


def analyze(fname):
    monkeys = read_data(fname)
    modulo = math.prod(m.divisible_by for m in monkeys)
    for _ in range(10000):
        for monkey in monkeys:
            monkey.throw_to(monkeys, modulo)
    counts = [m.inspect_count for m in monkeys]
    scounts = sorted(counts)
    return counts, scounts[-2] * scounts[-1]


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
