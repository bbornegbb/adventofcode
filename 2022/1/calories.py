#!/usr/bin/env python


def analyze(filename="input.txt"):
    calories = 0
    maxcalories = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "":
                maxcalories = max(calories, maxcalories)
                calories = 0
            else:
                calories += int(line)
    return max(calories, maxcalories)


if __name__ == "__main__":
    print(analyze())
