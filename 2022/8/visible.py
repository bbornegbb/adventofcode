#!/usr/bin/env python

import pandas as pd


def read_data(fname):
    with open(fname) as f:
        for line in f:
            yield [int(i) for i in line.strip()]


def analyze(fname):
    df = pd.DataFrame(read_data(fname))
    visible_top = df > df.cummax().shift(1, fill_value=-1)
    visible_bottom = df > df[::-1].cummax()[::-1].shift(-1, fill_value=-1)
    visible_left = df > df.cummax(1).shift(1, axis=1, fill_value=-1)
    visible_right = df > df.loc[::, ::-1].cummax(1).loc[::, ::-1].shift(
        -1, axis=1, fill_value=-1
    )
    return visible_top | visible_bottom | visible_left | visible_right


if __name__ == "__main__":
    df = analyze("input.txt")
    print(df)
    print(df.sum().sum())
