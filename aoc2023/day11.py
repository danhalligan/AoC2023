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


def dist(pair, rows, cols, multiplier=1):
    (x1, y1), (x2, y2) = pair
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    tot = abs((x2 - x1)) + abs((y2 - y1))
    tot += sum([x in range(x1, x2 + 1) for x in rows]) * multiplier
    tot += sum([x in range(y1, y2 + 1) for x in cols]) * multiplier
    return tot


def part_a(data):
    r, c, g = parse_data(data)
    return sum(dist(x, r, c) for x in combinations(g, 2))


def part_b(data):
    r, c, g = parse_data(data)
    return sum(dist(x, r, c, 999999) for x in combinations(g, 2))
