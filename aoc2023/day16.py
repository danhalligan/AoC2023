# Here we use complex numbers for coordinates and directions of travel
U, D, R, L = -1, +1, +1j, -1j


def parse(data):
    return {
        complex(i, j): x
        for i, line in enumerate(data.splitlines())
        for j, x in enumerate(line)
    }


def maxima(tiles):
    mr = max(int(p.real) for p in tiles.keys())
    mi = max(int(p.imag) for p in tiles.keys())
    return mr, mi


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


def inbounds(p, mr, mi):
    return p.real >= 0 and p.imag >= 0 and p.real <= mr and p.imag <= mi


def shine(start, tiles):
    mr, mi = maxima(tiles)
    q = [start]
    seen = {start}
    while q:
        p, d = q.pop()
        for nd in reflect(d, tiles[p]):
            np = p + nd
            if inbounds(np, mr, mi) and (np, nd) not in seen:
                q += [(np, nd)]
                seen.add((np, nd))
    return len(set(p for p, _ in seen))


def part_a(data):
    return shine((0j, R), parse(data))


def part_b(data):
    tiles = parse(data)
    mr, mi = maxima(tiles)
    return max(
        max(shine((complex(r, 0), R), tiles) for r in range(mr + 1)),
        max(shine((complex(r, mi), L), tiles) for r in range(mr + 1)),
        max(shine((complex(0, i), D), tiles) for i in range(mi + 1)),
        max(shine((complex(mr, i), U), tiles) for i in range(mi + 1)),
    )
