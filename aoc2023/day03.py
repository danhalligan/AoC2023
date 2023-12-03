import re


def find_nums(lines):
    for i, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            yield {"num": int(m.group()), "loc": [i, list(range(*m.span()))]}


def find_chars(lines, regex):
    for i, line in enumerate(lines):
        for m in re.finditer(regex, line):
            yield (i, m.span()[0])


def neighbours(x, y):
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]


def pos_adjacent(x, y, syms):
    return any(nb in syms for nb in neighbours(x, y))


def num_adjacent(num, syms):
    x, ys = num
    return any(pos_adjacent(x, y, syms) for y in ys)


def part_a(data):
    lines = data.splitlines()
    syms = list(find_chars(lines, r"[^\d\.]"))
    tot = 0
    for num in find_nums(lines):
        if num_adjacent(num["loc"], syms):
            tot += num["num"]
    return tot


def part_b(data):
    lines = data.splitlines()
    nums = list(find_nums(lines))
    tot = 0
    for gear in find_chars(lines, r"\*"):
        adj = [num["num"] for num in nums if num_adjacent(num["loc"], [gear])]
        if len(adj) == 2:
            tot += adj[0] * adj[1]
    return tot
