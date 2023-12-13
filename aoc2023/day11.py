from itertools import combinations


def parse_data(data):
    lines = data.splitlines()
    rows = [i for i, x in enumerate(lines) if "#" not in x]
    cols = [i for i in range(len(lines[0])) if "#" not in [x[i] for x in lines]]
    galaxies = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                galaxies += [(i, j)]
    return rows, cols, galaxies


def dist(a, b, gaps, multiplier):
    a, b = sorted([a, b])
    return (b - a) + sum([x in range(a, b + 1) for x in gaps]) * multiplier


def pair_dist(pair, rows, cols, multiplier=1):
    (x1, y1), (x2, y2) = pair
    return dist(x1, x2, rows, multiplier) + dist(y1, y2, cols, multiplier)


def part_a(data):
    r, c, g = parse_data(data)
    return sum(pair_dist(x, r, c) for x in combinations(g, 2))


def part_b(data):
    r, c, g = parse_data(data)
    return sum(pair_dist(x, r, c, 999999) for x in combinations(g, 2))
