#!/usr/bin/env python

import pandas as pd


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield [int(i) for i in line.strip()]


def visibility_top(df):
    can_see = pd.DataFrame(1, df.index, df.columns)
    result = pd.DataFrame(0, df.index, df.columns)
    for i in range(1, len(df)):
        shifted = df.shift(i, fill_value=10)
        result += can_see & (shifted < 10)
        can_see &= df > shifted
    return result


def visibility_bottom(df):
    return visibility_top(df[::-1])


def visibility_left(df):
    return visibility_top(df.T).T


def visibility_right(df):
    return visibility_left(df.loc[:, ::-1])


def analyze(fname):
    df = pd.DataFrame(read_data(fname))
    vl = visibility_left(df)
    vr = visibility_right(df)
    vt = visibility_top(df)
    vb = visibility_bottom(df)
    return vl * vr * vt * vb


if __name__ == "__main__":
    df = analyze("input.txt")
    print(df.max().max())
