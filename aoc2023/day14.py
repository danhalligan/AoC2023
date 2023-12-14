def parse(data):
    return {
        (i, j): x
        for i, line in enumerate(data.splitlines())
        for j, x in enumerate(line)
    }


# This fundtion rolls rocks, taking a list of list of tuples corresponding
# to the indices in the array to consider.
# This allows us to roll rocks in all 4 directions...
def roll(rocks, vals):
    for row in vals:
        gaps = []
        for val in row:
            if rocks[val] == ".":
                gaps += [val]
            elif rocks[val] == "#":
                gaps = []
            elif len(gaps):
                rocks[gaps.pop(0)] = "O"
                rocks[val] = "."
                gaps += [val]


# Calculate the "total load" for a configuration of rocks
def load(rocks):
    maxi = max(i for i, _ in rocks.keys())
    maxj = max(j for _, j in rocks.keys())
    tot = 0
    for i in range(maxi + 1):
        tot += (maxi - i + 1) * sum(rocks[i, j] == "O" for j in range(maxj + 1))
    return tot


def part_a(data):
    rocks = parse(data)
    maxi = max(i for i, _ in rocks.keys())
    maxj = max(j for _, j in rocks.keys())
    vals = [[(i, j) for i in range(maxi + 1)] for j in range(maxj + 1)]
    roll(rocks, vals)
    return load(rocks)


# Roll rocks in all 4 directions
def cycle(rocks):
    maxi = max(i for i, _ in rocks.keys())
    maxj = max(j for _, j in rocks.keys())
    vals = [[(i, j) for i in range(maxi + 1)] for j in range(maxj + 1)]
    roll(rocks, vals)
    vals = [[(i, j) for j in range(maxj + 1)] for i in range(maxi + 1)]
    roll(rocks, vals)
    vals = [[(i, j) for i in range(maxi, -1, -1)] for j in range(maxj + 1)]
    roll(rocks, vals)
    vals = [[(i, j) for j in range(maxj, -1, -1)] for i in range(maxi + 1)]
    roll(rocks, vals)


# Calculate a hash of a configuration of rocks
# This is unique for a given configuration (which load is not!)
def rockhash(rocks):
    return hash(frozenset(rocks.items()))


# Generate cycles, where each cycle rolls rocks in all 4 directions
def cycles(rocks):
    while True:
        cycle(rocks)
        yield rockhash(rocks)


# The goal here is to find a point when a rock hash repeats itself
# (occurs twice). We will then have a "burn in" period to get to this value
# first time, then a repeat size.
# This allows us to extrapolate to any future number of cycles...
def part_b(data):
    rocks = parse(data)
    hashes = [rockhash(rocks)]
    loads = [load(rocks)]

    for val in cycles(rocks):
        if sum(val == x for x in hashes) == 2:
            break
        hashes += [val]
        loads += [load(rocks)]

    burn_in, cycle_length = [i for i, x in enumerate(hashes) if val == x]
    return loads[burn_in + ((1000000000 - burn_in) % (cycle_length - burn_in))]
