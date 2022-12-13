#!/usr/bin/env python


def read_data(fname):
    with open(fname) as f:
        data = f.read()
    for tpl in data.split("\n\n"):
        left, right = tpl.strip().split("\n")
        l = eval(left)
        r = eval(right)
        yield l, r


# compares only integers
def cmp(l, r):
    if l < r:
        return -1
    if l == r:
        return 0
    else:  # l > r
        return 1


def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        return cmp(l, r)
    elif isinstance(l, list) and isinstance(r, list):
        for li, ri in zip(l, r):
            c = compare(li, ri)
            if c < 0:
                return -1
            elif c > 0:
                return 1
        return cmp(len(l), len(r))
    elif isinstance(l, int) and isinstance(r, list):
        return compare([l], r)
    elif isinstance(l, list) and isinstance(r, int):
        return compare(l, [r])
    else:
        raise ValueError(
            f"Don't know how to compare {l!r} with {r!r}\n"
            f"type(l) = {type(l)}  type(r) = {type(r)}"
        )


def analyze(fname):
    s = 0
    for i, (left, right) in enumerate(read_data(fname)):
        outcome = compare(left, right)
        if outcome < 0:
            s += i + 1
    return s


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
