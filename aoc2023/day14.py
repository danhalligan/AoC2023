def parse(data):
    return {
        (i, j): x
        for i, line in enumerate(data.splitlines())
        for j, x in enumerate(line)
    }


# This function rolls rocks, taking a list of list of tuples corresponding to the
# indices in the array to consider. This allows us to roll rocks in all 4 directions...
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


def limits(rocks):
    return max(i for i, _ in rocks.keys()), max(j for _, j in rocks.keys())


# Calculate the "total load" for a configuration of rocks
def load(rocks):
    maxi, maxj = limits(rocks)
    return sum(
        (maxi - i + 1) * sum(rocks[i, j] == "O" for j in range(maxj + 1))
        for i in range(maxi + 1)
    )


def part_a(data):
    rocks = parse(data)
    maxi, maxj = limits(rocks)
    vals = [[(i, j) for i in range(maxi + 1)] for j in range(maxj + 1)]
    roll(rocks, vals)
    return load(rocks)


# Roll rocks in all 4 directions
def cycle(rocks):
    maxi, maxj = limits(rocks)
    vals = [[(i, j) for i in range(maxi + 1)] for j in range(maxj + 1)]
    roll(rocks, vals)
    vals = [[(i, j) for j in range(maxj + 1)] for i in range(maxi + 1)]
    roll(rocks, vals)
    vals = [[(i, j) for i in range(maxi, -1, -1)] for j in range(maxj + 1)]
    roll(rocks, vals)
    vals = [[(i, j) for j in range(maxj, -1, -1)] for i in range(maxi + 1)]
    roll(rocks, vals)


# The goal here is to find a point when a rock layout repeats itself. To do this, we
# store a hash of a configuration of rocks. This is unique for a given configuration
# (which load is not!) We then calculate a "burn in" period to get to the first value
# and the cycle length till we get to it again. This allows us to extrapolate to any
# future number of cycles...
def part_b(data):
    rocks = parse(data)
    hashes, loads = [], []

    while True:
        val = hash(frozenset(rocks.items()))
        if hashes.count(val) == 2:
            break
        hashes += [val]
        loads += [load(rocks)]
        cycle(rocks)

    burn_in, repeat = [i for i, x in enumerate(hashes) if val == x]
    cycle_length = repeat - burn_in
    return loads[burn_in + ((1_000_000_000 - burn_in) % cycle_length)]
