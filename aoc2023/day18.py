import re
from itertools import pairwise


lookup = {"U": -1, "D": 1, "R": 1j, "L": -1j}


def part_a(data):
    grid = {}
    pos = 0j
    for line in data.splitlines():
        d, l, c = re.match(r"(.)\s(\d+)\s\((.+)\)", line).groups()
        for _ in range(int(l)):
            grid[pos] = c
            pos += lookup[d]

    # Flood fill from the interior (guessing an interior point)
    start = 1 + 1j
    queue = [start]
    while queue:
        p = queue.pop(0)
        for d in lookup.values():
            np = p + d
            if np not in grid:
                grid[np] = True
                queue.append(np)
    return len(grid)


def shoelace(v):
    s1 = sum(x1.real * x2.imag for x1, x2 in pairwise(v + [v[-1]]))
    s2 = sum(x2.real * x1.imag for x1, x2 in pairwise(v + [v[-1]]))
    return abs(s1 - s2) / 2


# We need to be smarter here.
# Shoelace formula and Pick's theorum are the way to go...
def part_b(data):
    vertices = [0j]
    boundary = 0
    for line in data.splitlines():
        d, l, c = re.match(r"(.)\s(\d+)\s\((.+)\)", line).groups()
        l = int(c[1:-1], 16)
        d = ["R", "D", "L", "U"][int(c[-1], 16)]
        boundary += l
        vertices += [vertices[-1] + lookup[d] * l]
    return int(shoelace(vertices) + boundary // 2 + 1)
