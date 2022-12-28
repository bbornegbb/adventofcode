#!/usr/bin/env python

import collections
import functools
import itertools
import re

import pulp


LINE_PATTERN = (
    r"Blueprint (?P<id>\d+): Each ore robot costs (?P<ore_ore>\d+) ore. "
    r"Each clay robot costs (?P<clay_ore>\d+) ore. "
    r"Each obsidian robot costs (?P<obsidian_ore>\d+) ore "
    r"and (?P<obsidian_clay>\d+) clay. "
    r"Each geode robot costs (?P<geode_ore>\d+) ore "
    r"and (?P<geode_obsidian>\d+) obsidian."
)

MINUTES = list(range(33))
RESOURCES = ORE, CLAY, OBSIDIAN, GEODE = "ore clay obsidian geode".split()

Blueprint = collections.namedtuple(
    "Blueprint",
    "id ore_ore clay_ore obsidian_ore obsidian_clay geode_ore geode_obsidian",
)


def blueprint_dict(blueprint):
    d = collections.defaultdict(dict)
    for robot, resource in itertools.product(RESOURCES, RESOURCES):
        attr = f"{robot}_{resource}"
        d[robot][resource] = getattr(blueprint, attr) if hasattr(blueprint, attr) else 0
    return dict(d)


def read_data(fname):
    r = re.compile(LINE_PATTERN)
    with open(fname) as f:
        for line in f:
            yield Blueprint(
                **{k: int(v) for k, v in r.match(line.strip()).groupdict().items()}
            )


def explain(cost, robots, stock):
    def fmt(c):
        return " and ".join(f"{v} {r}" for r, v in c.items() if v > 0)

    for m1, m2 in itertools.pairwise(MINUTES):
        print(f"== Minute {m1+1}")
        for r in RESOURCES:
            delta = robots[r][m2].value() - robots[r][m1].value()
            if delta > 0:
                print(f"Spend {fmt(cost[r])} to start building a {r}-collecting robot.")
        for r in RESOURCES:
            cnt = robots[r][m1].value()
            if cnt > 0:
                print(
                    f"{cnt} {r}-collecting robots collect {cnt} ore; "
                    f"you now have {stock[r][m2].value()} {r}."
                )
        for r in RESOURCES:
            delta = robots[r][m2].value() - robots[r][m1].value()
            if delta > 0:
                print(
                    f"The new {r}-collecting robot is ready; "
                    f"you now have {robots[r][m2].value()} of them."
                )
        print()


def evaluate(blueprint):
    cost = blueprint_dict(blueprint)
    problem = pulp.LpProblem(f"Geodes Problem {blueprint}", pulp.LpMaximize)
    robots = pulp.LpVariable.dicts(
        "robots", (RESOURCES, MINUTES), lowBound=0, cat=pulp.LpInteger
    )
    stock = pulp.LpVariable.dicts(
        "stock", (RESOURCES, MINUTES), lowBound=0, cat=pulp.LpInteger
    )
    optimize_for = stock[GEODE][32]
    problem += optimize_for
    problem += robots[ORE][0] == 1
    for resource in RESOURCES[1:]:
        problem += robots[resource][0] == 0
    for resource in RESOURCES:
        problem += stock[resource][0] == 0
        for m1, m2 in itertools.pairwise(MINUTES):
            construction_cost = (
                (robots[ORE][m2] - robots[ORE][m1]) * cost[ORE][resource]
                + (robots[CLAY][m2] - robots[CLAY][m1]) * cost[CLAY][resource]
                + (robots[OBSIDIAN][m2] - robots[OBSIDIAN][m1])
                * cost[OBSIDIAN][resource]
                + (robots[GEODE][m2] - robots[GEODE][m1]) * cost[GEODE][resource]
            )
            # We can only build robots, never destruct them
            problem += robots[resource][m1] <= robots[resource][m2]
            # New stock is old stock plus collection minus building cost
            problem += (
                stock[resource][m2]
                == stock[resource][m1] + robots[resource][m1] - construction_cost
            )
            # Stock in m1 needs to be large enough to build for m2
            problem += stock[resource][m1] >= construction_cost
    # We can build only one robot per iteration - this is not documented but
    # we can easily test with the second test blueprint
    for m1, m2 in itertools.pairwise(MINUTES):
        problem += (
            sum(robots[resource][m2] - robots[resource][m1] for resource in RESOURCES)
            <= 1
        )
    problem.solve()
    assert pulp.LpStatus[problem.status] == "Optimal"
    # explain(cost, robots, stock)
    return optimize_for.value()


def analyze(fname):
    data = read_data(fname)
    quality = []
    for blueprint, _ in zip(data, range(3)):
        print(blueprint)
        max_geodes = evaluate(blueprint)
        quality.append((blueprint.id, max_geodes))
    return quality, functools.reduce(lambda x, y: x * y, (g for _, g in quality))


if __name__ == "__main__":
    # print(analyze("test.txt"))
    print(analyze("input.txt"))
