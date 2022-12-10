#!/usr/bin/env python

from collections import namedtuple

Move = namedtuple("Move", "count from_ to")


def read_stacks(fhandle):
    lines = []
    for line in fhandle:
        line = line.rstrip("\n")
        if line == "":
            break
        lines.append(line)
    stack_names = lines[-1].split()
    stacks = [list() for n in stack_names]
    for line in lines[-2::-1]:
        # fast but not very robust
        stack_items = line[1::4]
        for i, stack_item in enumerate(stack_items):
            if stack_item != " ":
                stacks[i].append(stack_item)
    return stack_names, stacks


def read_moves(fhandle):
    moves = []
    for line in fhandle:
        _, cnt, _, from_, _, to = line.split()
        moves.append(Move(int(cnt), int(from_), int(to)))
    return moves


def print_moves(moves):
    for move in moves:
        print(move)


def execute_moves(stacks, moves):
    for move in moves:
        fromstack = stacks[move.from_ - 1]
        tostack = stacks[move.to - 1]
        cnt = move.count
        tostack.extend(fromstack[-cnt:])
        fromstack[-cnt:] = []


def print_stacks(stacks):
    for stack in stacks:
        print(stack)


def print_top_of_stacks(stacks):
    print("".join(stack[-1] for stack in stacks if len(stack) > 0))


def analyze(fname):
    with open(fname) as f:
        names, stacks = read_stacks(f)
        moves = read_moves(f)
    execute_moves(stacks, moves)
    print_stacks(stacks)
    print_moves(moves)
    print_stacks(stacks)
    print_top_of_stacks(stacks)


if __name__ == "__main__":
    analyze("input.txt")
    # analyze("test.txt")
