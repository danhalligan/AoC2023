import numpy as np
import os

U, D, R, L = -1, +1, +1j, -1j


def parse(data):
    grid = {}
    for i, line in enumerate(data.splitlines()):
        for j, x in enumerate(line):
            grid[complex(i, j)] = x
            if x == "S":
                start = complex(i, j)
                grid[complex(i, j)] = "."
    return grid, start


def step(grid, pos):
    newpos = set()
    for p in pos:
        for d in [U, D, R, L]:
            if p + d in grid and grid[p + d] == ".":
                newpos.add((p + d))
    return newpos


def part_a(data):
    grid, start = parse(data)
    pos = [start]
    s = 6 if "PYTEST_CURRENT_TEST" in os.environ else 64
    for _ in range(s):
        pos = step(grid, pos)
    return len(pos)


def parse2(data):
    grid = set()
    for i, line in enumerate(data.splitlines()):
        for j, x in enumerate(line):
            if x == "#":
                grid.add(complex(i, j))
            if x == "S":
                start = complex(i, j)
    return grid, start


def wrap(p):
    return complex(p.real % 131, p.imag % 131)


def step2(grid, pos):
    newpos = set()
    for p in pos:
        for d in [U, D, R, L]:
            if wrap(p + d) not in grid:
                newpos.add(p + d)
    return newpos


# This problem eluded me. I've adapted the solution here
# https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaq9zk/
#
# We're asked to find the solution when t = 26501365
# 26501365 is exactly 131 * 202300 + 65
# Additionally, number of plots (n) follows a polynomial function in t=131*2 increments
# We can recover this function based on the first 3 values
def part_b(data):
    grid, start = parse2(data)
    pos = [start]

    X, Y = [0, 1, 2], []
    target = 202300
    for s in range(65 + 131 * 2 + 1):
        if s % 131 == 65:
            Y.append(len(pos))
        pos = step2(grid, pos)

    poly = np.rint(np.polynomial.polynomial.polyfit(X, Y, 2)).astype(int).tolist()
    return sum(poly[i] * target**i for i in range(3))
