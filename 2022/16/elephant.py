#!/usr/bin/env python


import collections
import itertools
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

MAX_TIME = 26


def read_data(fname):
    r = re.compile(LINE_PATTERN)
    with open(fname) as f:
        for line in f:
            match = r.match(line.strip())
            gd = match.groupdict()
            tunnels = tuple(gd["tunnels"].split(", "))
            yield Valve(gd["name"], int(gd["rate"]), tunnels)


def search(G, loc, targets, target_rates, minute=0):
    best_relief = -1
    for target in targets:
        path = nx.shortest_path(G, loc, target)
        # (len(path) - 1) minutes to get there, 1 minute to enable flow
        time_to_enable = len(path)
        new_minute = minute + time_to_enable
        if new_minute >= MAX_TIME:
            continue
        remaining_targets = [t for t in targets if t != target]
        remaining_flow_potential = sum(
            target_rates[t] * (MAX_TIME - new_minute - i - 1)
            for i, t in enumerate(
                sorted(remaining_targets, key=lambda x: -target_rates[x])
            )
        )
        my_relief = (MAX_TIME - new_minute) * target_rates[target]
        if best_relief > my_relief + remaining_flow_potential:
            continue
        found_relief, actions = search(
            G, target, remaining_targets, target_rates, new_minute
        )
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


def build_graph(data):
    G = nx.Graph()
    for v in data:
        G.add_node(v.name, rate=v.rate)
    for v in data:
        G.add_edges_from((v.name, tun) for tun in v.tunnels)
    return G


def partition_work(data):
    s = set(data)
    l = len(s)
    for w in itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(l // 2 + 1)
    ):
        yield w, tuple(s - set(w))


def analyze(fname):
    data = list(read_data(fname))
    G = build_graph(data)
    if False:
        labels = nx.get_node_attributes(G, "rate")
        labels = {k: f"{k} {v}" for k, v in labels.items()}
        nx.draw_networkx(G, labels=labels, font_color="w", node_size=1500)
        plt.show()
    targets = list(
        v.name for v in sorted(data, key=operator.attrgetter("rate")) if v.rate > 0
    )
    target_rates = {v.name: v.rate for v in data if v.rate > 0}
    best_flow = -1
    for t1, t2 in partition_work(targets):
        f1, _ = search(G, "AA", t1[::-1], target_rates, 0)
        f2, _ = search(G, "AA", t2[::-1], target_rates, 0)
        f = f1 + f2
        if f > best_flow:
            best_flow = f
            best_partition = (t1, t2)

    return {
        "degree": G.degree,
        "valves": data,
        "rates": sorted(v.rate for v in data),
        "best_flow": best_flow,
        "best_partition": best_partition,
    }


if __name__ == "__main__":
    # pprint(analyze("test.txt"))
    pprint(analyze("input.txt"))
