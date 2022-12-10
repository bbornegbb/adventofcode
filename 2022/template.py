#!/usr/bin/env python


def read_data(fname):
    with open(fname) as f:
        pass


def analyze(fname):
    data = read_data(fname)
    return data


if __name__ == "__main__":
    print(analyze("test.txt"))
    # print(analyze("input.txt"))
