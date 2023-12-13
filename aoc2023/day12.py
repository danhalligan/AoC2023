from functools import cache


def drop1(counts):
    return tuple([counts[0] - 1] + list(counts[1:]))


# `in_run` tracks if we're in a run of "#"s (in other words, if last character
# was a "#")
@cache
def complete(txt, counts, in_run=False):
    if not len(txt):
        # At end of sequence. counts should be empty
        return int(len(counts) == 0 or (len(counts) == 1 and counts[0] == 0))
    elif txt[0] == "#":
        if len(counts) and counts[0] >= 1:
            return complete(txt[1:], drop1(counts), True)
    elif txt[0] == ".":
        if in_run:
            if counts[0] == 0:
                return complete(txt[1:], counts[1:])
        else:
            return complete(txt[1:], counts)
    elif txt[0] == "?":
        if len(counts) == 0:
            # no counts left -- must insert "."
            return complete(txt[1:], counts)
        elif counts[0] == 0:
            # we're at end of run so must insert a "."
            return complete(txt[1:], counts[1:])
        else:
            tot = complete(txt[1:], drop1(counts), True)
            if not in_run:
                tot += complete(txt[1:], counts)
            return tot
    return 0


def solve(data, b=False):
    tot = 0
    for line in data.splitlines():
        txt, counts = line.split(" ")
        if b:
            txt = "?".join([txt] * 5)
            counts = ",".join([counts] * 5)
        counts = [int(x) for x in counts.split(",")]
        tot += complete(txt, tuple(counts))
    return tot


def part_a(data):
    return solve(data)


def part_b(data):
    return solve(data, True)
