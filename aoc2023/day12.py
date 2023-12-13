# from more_itertools import distinct_permutations
# from itertools import groupby
from functools import cache


# Nasty original hack commented...
# def rle(txt, repl):
#     k = 0
#     txt = list(txt)
#     for i in range(len(txt)):
#         if txt[i] == "?":
#             txt[i] = repl[k]
#             k += 1
#     return [len(list(y)) for x, y in groupby(txt) if x == "#"]
#
#
# def part_a(data):
#     tot = 0
#     for line in data.splitlines():
#         txt, counts = line.split(" ")
#         counts = [int(x) for x in counts.split(",")]
#         nbroken = sum(counts) - txt.count("#")
#         nmissing = txt.count("?")
#         v = ["#"] * nbroken + ["."] * (nmissing - nbroken)
#         tot += len(
#             [p for p in distinct_permutations(v, len(v)) if rle(txt, p) == counts]
#         )
#     return tot


def drop1(counts):
    return tuple([counts[0] - 1] + list(counts[1:]))


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
