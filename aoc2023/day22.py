from copy import deepcopy


def overlaps(x, y):
    return max(x.start, y.start) < min(x.stop, y.stop)


def will_hit(b1, b2):
    return overlaps(b1["x"], b2["x"]) and overlaps(b1["y"], b2["y"])


def drop(b, n):
    b["z"] = range(b["z"].start - n, b["z"].stop - n)


def parse(data):
    bricks = []
    for line in data.splitlines():
        a, b = line.split("~")
        a = [int(x) for x in a.split(",")]
        b = [int(x) for x in b.split(",")]
        rx = range(a[0], b[0] + 1)
        ry = range(a[1], b[1] + 1)
        rz = range(a[2], b[2] + 1)
        bricks.append({"x": rx, "y": ry, "z": rz})
    return bricks


def drop_bricks(bricks):
    # drop all bricks by working from bottom brick up
    n_dropped = 0
    for i, brick in enumerate(bricks):
        zs = [max(bricks[j]["z"]) for j in range(i) if will_hit(brick, bricks[j])]
        zs += [0]
        if min(brick["z"]) > max(zs) + 1:
            # print("dropping", i, "by", min(brick["z"]) - (max(zs) + 1))
            drop(brick, min(brick["z"]) - (max(zs) + 1))
            n_dropped += 1
    return n_dropped


def part_a(data):
    bricks = parse(data)
    bricks.sort(key=lambda x: min(x["z"]))  # sort bricks by min z-coordinate
    drop_bricks(bricks)

    count = 0
    for candidate in range(len(bricks)):
        supports = False
        for i in range(candidate, len(bricks)):  # brick that could be dropped
            zs = [0]
            for j in range(i):  # potential supporting bricks
                if j == candidate:
                    continue
                if will_hit(bricks[i], bricks[j]):
                    zs.append(max(bricks[j]["z"]))
            if zs and min(bricks[i]["z"]) > max(zs) + 1:
                # print("cand", candidate, "supports", i)
                supports = True
                break
        if not supports:
            count += 1
    return count


# This is a horrible brute force type approach that runs v slowly...
# I literally clone all bricks, remove a brick and then see how many will drop
def part_b(data):
    bricks = parse(data)
    bricks.sort(key=lambda x: min(x["z"]))  # sort bricks by min z-coordinate
    drop_bricks(bricks)
    tot = 0
    for candidate in range(len(bricks)):
        bricks_tmp = deepcopy(bricks)
        bricks_tmp = bricks_tmp[:candidate] + bricks_tmp[candidate + 1 :]
        n = drop_bricks(bricks_tmp)
        tot += n
    return tot
