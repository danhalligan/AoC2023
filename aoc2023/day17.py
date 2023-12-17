from heapq import heappop, heappush

# Here we use complex numbers for coordinates and directions of travel
U, D, R, L = -1, +1, +1j, -1j


def parse(data):
    return {
        complex(i, j): int(x)
        for i, line in enumerate(data.splitlines())
        for j, x in enumerate(line)
    }


def maxima(tiles):
    mr = max(p.real for p in tiles.keys())
    mi = max(p.imag for p in tiles.keys())
    return complex(mr, mi)


# Reflection logic for different directions entering into a tile
def directions(d, count):
    nd = {R: [R, U, D], L: [L, U, D], U: [U, R, L], D: [D, R, L]}[d]
    if count == 3:
        nd.remove(d)
    return nd


def in_bounds(p, m):
    return p.real >= 0 and p.imag >= 0 and p.real <= m.real and p.imag <= m.imag


# h: heat score
# p: position (complex number)
# d: direction (complex number)
# c: direction count (moves in constant direction till now)
# e: an "entry count" to break ties when using heapq
def find_path(grid, dfn):
    m = maxima(grid)
    q = []
    heappush(q, (0, (0, 0j, R, 1)))
    heappush(q, (0, (1, 0j, D, 1)))
    e = 1
    seen = dict()
    while q:
        h, (_, p, d, c) = heappop(q)
        for nd in dfn(d, c):
            np = p + nd
            if in_bounds(np, m):
                nh = h + grid[np]
                nc = c + 1 if nd == d else 1
                if (np, nd, nc) not in seen or nh < seen[(np, nd, nc)][0]:
                    e += 1
                    heappush(q, (nh, (e, np, nd, nc)))
                    seen[(np, nd, nc)] = (nh, nc)
    return [x for k, x in seen.items() if k[0] == m]


def directions_ultra(d, count):
    if count < 4:
        return [d]
    nd = {R: [R, U, D], L: [L, U, D], U: [U, R, L], D: [D, R, L]}[d]
    if count == 10:
        nd.remove(d)
    return nd


def part_a(data):
    grid = parse(data)
    scores = find_path(grid, directions)
    return min(h for h, _ in scores)


def part_b(data):
    grid = parse(data)
    scores = find_path(grid, directions_ultra)
    return min(h for h, c in scores if c >= 4)
