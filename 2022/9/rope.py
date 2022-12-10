#!/usr/bin/env python


def read_data(fname):
    with open(fname) as f:
        for line in f:
            direction, amount = line.split()
            yield direction, int(amount)


class Loc(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def up(self):
        self.y += 1

    def down(self):
        self.y -= 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def getpos(self):
        return (self.x, self.y)


class Head(Loc):
    def __str__(self):
        return f"H({self.x}, {self.y})"


class Tail(Loc):
    def __str__(self):
        return f"T({self.x}, {self.y})"

    def follow(self, head):
        hx, hy = head.getpos()
        x, y = self.x, self.y
        dx = hx - x
        dy = hy - y
        distance = abs(dx) + abs(dy)
        if distance <= 1:
            pass
        elif dy == 0:
            if dx > 0:
                self.right()
            else:
                self.left()
        elif dx == 0:
            if dy > 0:
                self.up()
            else:
                self.down()
        elif abs(dx) == 1 and abs(dy) == 1:
            pass
        else:
            assert distance >= 3
            if dx > 0:
                self.right()
            else:
                self.left()
            if dy > 0:
                self.up()
            else:
                self.down()


def analyze(fname):
    data = read_data(fname)
    head = Head()
    tail = Tail()
    moves = {
        "U": head.up,
        "D": head.down,
        "L": head.left,
        "R": head.right,
    }
    visited = set()
    for direction, amount in data:
        for _ in range(amount):
            moves[direction]()
            tail.follow(head)
            visited.add(tail.getpos())
            print(direction, head, tail)
    return visited


if __name__ == "__main__":
    # print(len(analyze("test.txt")))
    print(len(analyze("input.txt")))
