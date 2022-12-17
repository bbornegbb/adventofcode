#!/usr/bin/env python


import collections
import operator
import re

from pprint import pprint

from matplotlib import pyplot as plt
import networkx as nx

# Example: Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
LINE_PATTERN = (
    r"Valve (?P<name>[A-Z]+) has flow rate=(?P<rate>\d+); "
    r"tunnels? leads? to valves? (?P<tunnels>[A-Z, ]+)$"
)

Valve = collections.namedtuple("Valve", "name rate tunnels")


def read_data(fname):
    r = re.compile(LINE_PATTERN)
    with open(fname) as f:
        for line in f:
            match = r.match(line.strip())
            gd = match.groupdict()
            tunnels = tuple(gd["tunnels"].split(", "))
            yield Valve(gd["name"], int(gd["rate"]), tunnels)


def search(G, loc, targets, minute=0):
    best_relief = -1
    for target in targets:
        path = nx.shortest_path(G, loc, target)
        # (len(path) - 1) minutes to get there, 1 minute to enable flow
        time_to_enable = len(path)
        new_minute = minute + time_to_enable
        if new_minute >= 30:
            continue
        remaining_targets = [t for t in targets if t != target]
        found_relief, actions = search(G, target, remaining_targets, new_minute)
        my_relief = (30 - new_minute) * G.nodes[target]["rate"]
        total_relief = my_relief + found_relief
        if total_relief > best_relief:
            best_relief = total_relief
            best_target = target
            best_path = path
            best_actions = actions
            best_minute = new_minute
    # We ran out of time
    if best_relief == -1:
        return 0, []
    actions_new = [f"Walk to {node}" for node in best_path[1:]]
    actions_new.append(
        f"Enable flow at {best_target} with rate {G.nodes[best_target]['rate']} at minute={best_minute}"
    )
    actions_new.extend(best_actions)
    return best_relief, actions_new


def analyze(fname):
    data = list(read_data(fname))
    G = nx.Graph()
    for v in data:
        G.add_node(v.name, rate=v.rate)
    for v in data:
        G.add_edges_from((v.name, tun) for tun in v.tunnels)
    if False:
        labels = nx.get_node_attributes(G, "rate")
        labels = {k: f"{k} {v}" for k, v in labels.items()}
        nx.draw_networkx(G, labels=labels, font_color="w", node_size=1500)
        plt.show()
    targets = list(
        v.name for v in sorted(data, key=operator.attrgetter("rate")) if v.rate > 0
    )
    return {
        "degree": G.degree,
        "valves": data,
        "rates": sorted(v.rate for v in data),
        "best_flow": search(G, "AA", targets[::-1], 0),
    }


if __name__ == "__main__":
    # pprint(analyze("test.txt"))
    pprint(analyze("input.txt"))
