# Here we use complex numbers for coordinates and directions of travel
U, D, R, L = -1, +1, +1j, -1j


def parse(data):
    return {
        complex(i, j): x
        for i, line in enumerate(data.splitlines())
        for j, x in enumerate(line)
    }


def maxima(tiles):
    mr = max(p.real for p in tiles.keys())
    mi = max(p.imag for p in tiles.keys())
    return complex(mr, mi)


# Reflection logic for different directions entering into a tile
def reflect(d, tile):
    if d == R:
        return {".": [R], "-": [R], "\\": [D], "/": [U], "|": [D, U]}[tile]
    if d == L:
        return {".": [L], "-": [L], "\\": [U], "/": [D], "|": [D, U]}[tile]
    if d == U:
        return {".": [U], "-": [L, R], "\\": [L], "/": [R], "|": [U]}[tile]
    if d == D:
        return {".": [D], "-": [L, R], "\\": [R], "/": [L], "|": [D]}[tile]


def in_bounds(p, m):
    return p.real >= 0 and p.imag >= 0 and p.real <= m.real and p.imag <= m.imag


def shine(start, tiles):
    m = maxima(tiles)
    q = [start]
    seen = {start}
    while q:
        p, d = q.pop()
        for nd in reflect(d, tiles[p]):
            np = p + nd
            if in_bounds(np, m) and (np, nd) not in seen:
                q += [(np, nd)]
                seen.add((np, nd))
    return len(set(p for p, _ in seen))


def part_a(data):
    return shine((0j, R), parse(data))


def part_b(data):
    tiles = parse(data)
    m = maxima(tiles)
    rr = range(int(m.real) + 1)
    ri = range(int(m.imag) + 1)
    starts = (
        [(complex(r, 0), R) for r in rr]
        + [(complex(r, m.imag), L) for r in rr]
        + [(complex(0, i), D) for i in ri]
        + [(complex(m.real, i), U) for i in ri]
    )
    return max(shine(s, tiles) for s in starts)
