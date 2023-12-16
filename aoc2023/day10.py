from collections import defaultdict
from itertools import pairwise


def neighbours(pos, data):
    x, y = pos
    if data[pos] in "|LJ" and data[x - 1, y] in "|7F":
        yield x - 1, y
    if data[pos] in "-LF" and data[x, y + 1] in "-J7":
        yield x, y + 1
    if data[pos] in "|7F" and data[x + 1, y] in "|LJ":
        yield x + 1, y
    if data[pos] in "-7J" and data[x, y - 1] in "-LF":
        yield x, y - 1


def parse_data(data):
    grid = defaultdict(lambda: ".")
    start = None
    for x, row in enumerate(data.splitlines()):
        for y, pos in enumerate(row):
            grid[x, y] = pos
            if pos == "S":
                start = (x, y)
    return start, grid


# Try to follow path
def try_path(start, data):
    visited = {start: 0}
    queue = [start]
    while queue:
        pos = queue.pop(0)
        nbs = [nb for nb in neighbours(pos, data) if nb not in visited]
        if nbs:
            nb = nbs[0]
            visited[nb] = visited[pos] + 1
            queue.append(nb)
    return visited


def find_path(start, data):
    for opt in ["|", "-", "L", "J", "7", "F"]:
        data[start] = opt
        visited = try_path(start, data)
        if len(visited) > 1:
            return visited


# Expand path by doubling coordinates. This way, we can flood fill from the outside and
# we'll reach all cells considered exterior to path.
def expand_path(path):
    expanded = set()
    for x in path:
        expanded.add((x[0] * 2, x[1] * 2))
    for p1, p2 in pairwise(path + [path[0]]):
        expanded.add((p1[0] + p2[0], p1[1] + p2[1]))
    return expanded


# When flood filling we pad 1 cell all the way around the path. We start from -1,-1
# (definitely not in the path)
def flood(path):
    start = (-1, -1)
    mx = max(x for x, _ in path)
    my = max(y for _, y in path)
    seen = set([start])
    queue = [start]
    while queue:
        x, y = queue.pop(0)
        for nx, ny in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:
            if nx >= -1 and ny >= -1 and nx <= mx + 1 and ny <= my + 1:
                if (nx, ny) not in path and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    queue.append((nx, ny))
    return seen


def part_a(data):
    start, data = parse_data(data)
    visited = find_path(start, data)
    return len(visited) // 2


def part_b(data):
    start, data = parse_data(data)
    visited = find_path(start, data)
    expanded = expand_path(list(visited.keys()))
    outside = flood(expanded)
    count = 0
    mx = max(x for x, _ in outside)
    my = max(y for _, y in outside)
    for i in range(0, mx, 2):
        for y in range(0, my, 2):
            if (i, y) not in outside and (i, y) not in expanded:
                count += 1
    return count
