#!/usr/bin/env python


def read_test(fname):
    with open(fname) as f:
        h1, h2 = next(f).strip().split()
        if h1 == "Decimal":
            for line in f:
                yield line.strip().split()[::-1]
        else:
            for line in f:
                yield line.strip().split()


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield line.strip()


s2d = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

d2s = {v: k for k, v in s2d.items()}


def snafu2decimal(snafu):
    rv = 0
    for c in snafu:
        rv *= 5
        rv += s2d[c]
    return rv


def decimal2snafu(decimal):
    d, r = divmod(decimal, 5)
    if r > 2:
        d += 1
        r -= 5
    if d > 0:
        return decimal2snafu(d) + d2s[r]
    else:
        return d2s[r]


def test(fname):
    data = read_test(fname)
    for snafu, decimal in data:
        decimal = int(decimal)
        got_decimal = snafu2decimal(snafu)
        if decimal != got_decimal:
            print(f"snafu2decimal({snafu!r} = {got_decimal!r}, want {decimal!r}")
        got_snafu = decimal2snafu(decimal)
        if snafu != got_snafu:
            print(f"decimal2snafu({decimal!r} = {got_snafu!r}, want {snafu!r}")


def analyze(fname):
    data = read_data(fname)
    total = sum(snafu2decimal(l) for l in data)
    return total, decimal2snafu(total)


if __name__ == "__main__":
    # test("test.txt")
    # test("test2.txt")
    # print(analyze("test3.txt"))
    print(analyze("input.txt"))
