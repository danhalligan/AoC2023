from math import ceil, floor, prod, sqrt
from .helpers import ints


def n_ways(time, dist):
    hi = floor((sqrt(time**2 - 4 * dist) + time) / 2 - 0.1)
    lo = ceil((time - sqrt(time**2 - 4 * dist)) / 2 + 0.1)
    return hi - lo + 1


def part_a(data):
    data = data.splitlines()
    data = [ints(x) for x in data]
    return prod(n_ways(data[0][i], data[1][i]) for i in range(len(data[0])))


def part_b(data):
    data = data.splitlines()
    data = [ints(x) for x in data]
    time = int("".join([str(x) for x in data[0]]))
    dist = int("".join([str(x) for x in data[1]]))
    return n_ways(time, dist)
