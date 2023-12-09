import re
from .helpers import ints


def try_map(val, m):
    if val >= m[1] and val < (m[1] + m[2]):
        return m[0] + (val - m[1])


def do_map(val, maps):
    for m in maps:
        new = try_map(val, m)
        if new is not None:
            return new
    return val


def parse_section(section):
    return [ints(x) for x in section.splitlines()][1:]


def part_a(data):
    sections = data.split("\n\n")
    seeds = ints(sections[0])
    sections = [parse_section(x) for x in sections[1:]]
    vals = seeds
    for section in sections:
        vals = [do_map(val, section) for val in vals]

    return min(vals)


# ------------------------------------------------------------------------------
def intersection(r1, r2):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop + 1))


def map_range(src, fr, to):
    offset = to.start - fr.start
    return range(src.start + offset, src.stop + offset)


# convert each section of maps to from and to ranges.
# actually we probably just need source range and offset
def convert_section(section):
    return [[range(x[1], x[1] + x[2]), range(x[0], x[0] + x[2])] for x in section]


# convert seeds to ranges
def convert_seeds(seeds):
    for i in list(range(0, len(seeds), 2)):
        yield range(seeds[i], seeds[i] + seeds[i + 1])


# Take a source range (e.g. of seeds), and try to map with all maps in a
# section. We need to track ranges of values that are not mapped with each map
# Any of these that are left at the end are added to the mapped ranges.
def map_source(ra, section):
    tomap = [ra]
    mapped = []
    for src, dest in section:
        unmapped = []
        for ra in tomap:
            overlap = intersection(ra, src)
            if len(overlap):
                mapped += [map_range(overlap, src, dest)]
            if ra.start < src.start:
                unmapped += [range(ra.start, min(ra.stop, src.start))]
            if ra.stop > src.stop:
                unmapped += [range(max(ra.start, src.stop), ra.stop)]
        tomap = unmapped
    return mapped + unmapped


def part_b(data):
    sections = data.split("\n\n")
    seeds = ints(sections[0])
    sections = [parse_section(x) for x in sections[1:]]
    seeds = list(convert_seeds(seeds))
    sections = [convert_section(x) for x in sections]

    vals = seeds
    for section in sections:
        vals = [map_source(ra, section) for ra in vals]
        vals = [item for sublist in vals for item in sublist]

    return min(ra.start for ra in vals)
