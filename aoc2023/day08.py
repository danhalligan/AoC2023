import re
from itertools import cycle
from math import lcm


def parse_node(line):
    parts = re.findall(r"\w\w\w", line)
    return parts[0], {"L": parts[1], "R": parts[2]}


def parse_data(data):
    instructions, nodes = data.split("\n\n")
    instructions = list(instructions)
    nodes = dict(parse_node(line) for line in nodes.splitlines())
    return instructions, nodes


def part_a(data):
    instructions, nodes = parse_data(data)
    node = "AAA"
    steps = 0
    for x in cycle(instructions):
        node = nodes[node][x]
        steps += 1
        if node == "ZZZ":
            break
    return steps


# Here I guessed that following instructions from each starting point formed a
# cycle back to itself. If true, then all cycles end together at the lowest
# common multiple.
def part_b(data):
    instructions, nodes = parse_data(data)
    steps = {node: 0 for node in nodes.keys() if node.endswith("A")}
    for start in steps.keys():
        node = start
        for x in cycle(instructions):
            node = nodes[node][x]
            steps[start] += 1
            if node.endswith("Z"):
                break
    return lcm(*steps.values())
