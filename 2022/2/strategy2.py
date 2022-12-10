#!/usr/bin/env python

shape2value = {"X": 1, "Y": 2, "Z": 3}

draw = ("A X", "B Y", "C Z")
win = ("A Y", "B Z", "C X")
# lose = ('A Z', 'B X', 'C Y')
action = {
    "A X": "Z",
    "A Y": "X",
    "A Z": "Y",
    "B X": "X",
    "B Y": "Y",
    "B Z": "Z",
    "C X": "Y",
    "C Y": "Z",
    "C Z": "X",
}


def analyze(fname="input.txt"):
    score = 0
    with open(fname) as f:
        for line in f:
            line = line.strip()
            # assert line in (draw+win+lose), f"'{line}' is not a match'"
            op, me = line.split()
            line = f"{op} {action[line]}"
            if line in win:
                score += 6
            elif line in draw:
                score += 3
            score += shape2value[line.split()[1]]
    return score


if __name__ == "__main__":
    print(analyze())
