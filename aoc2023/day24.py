from itertools import combinations
from z3 import Solver, Real
import os


def parse(data):
    hail = []
    for line in data.splitlines():
        pos, vel = [[int(x) for x in y.split(", ")] for y in line.split(" @ ")]
        hail.append({"pos": pos, "vel": vel})
    return hail


def intersection(h1, h2):
    a1 = h1["vel"][1] / h1["vel"][0]
    b1 = h1["pos"][1] - a1 * h1["pos"][0]
    a2 = h2["vel"][1] / h2["vel"][0]
    b2 = h2["pos"][1] - a2 * h2["pos"][0]
    xi = (b1 - b2) / (a2 - a1)
    yi = a1 * xi + b1
    return xi, yi


def in_future(h, p):
    p1 = h["pos"]
    vel = h["vel"]
    n1 = [p1[0] + vel[0], p1[1] + vel[1]]
    dp1 = abs(p[0] - p1[0]) + abs(p[1] - p1[1])
    dn1 = abs(p[0] - n1[0]) + abs(p[1] - n1[1])
    return dp1 > dn1


def in_range(pos, min, max):
    return pos[0] >= min and pos[0] <= max and pos[1] >= min and pos[1] <= max


def part_a(data):
    hail = parse(data)
    if "PYTEST_CURRENT_TEST" in os.environ:
        minx, maxx = 7, 27
    else:
        minx, maxx = 200_000_000_000_000, 400_000_000_000_000
    tot = 0
    for h1, h2 in combinations(hail, 2):
        try:
            pi = intersection(h1, h2)
        except Exception:
            continue
        tot += in_range(pi, minx, maxx) and in_future(h1, pi) and in_future(h2, pi)
    return tot


# I got stuck here and looked to reddit for answers involving Z3.
# You only need enough hailstones to fully determine the unknowns in
# the system of equations...
def part_b(data):
    hail = parse(data)

    x, y, z = Real("x"), Real("y"), Real("z")
    vx, vy, vz = Real("vx"), Real("vy"), Real("vz")

    solver = Solver()

    for i, h in enumerate(hail[:3]):
        px, py, pz = h["pos"]
        pvx, pvy, pvz = h["vel"]
        t = Real(f"t{i}")
        solver.add(t >= 0)
        solver.add(x + vx * t == px + pvx * t)
        solver.add(y + vy * t == py + pvy * t)
        solver.add(z + vz * t == pz + pvz * t)

    solver.check()
    model = solver.model()
    res = [model.eval(x), model.eval(y), model.eval(z)]
    return sum(i.as_long() for i in res)
