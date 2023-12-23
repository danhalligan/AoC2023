import networkx as nx
from networkx.classes.function import path_weight

U, D, R, L = -1, +1, +1j, -1j


def parse(data):
    grid = {
        complex(i, j): x
        for i, line in enumerate(data.splitlines())
        for j, x in enumerate(line)
    }
    last = [*grid][-1]
    return grid, 1j, last + L


def part_a(data):
    grid, start, end = parse(data)
    dl = {">": R, "^": U, "v": D, "<": L}

    q = [(start, 0, [])]
    routes = {}
    while q:
        p, s, path = q.pop()
        for d in [U, D, L, R]:
            np = p + d
            if np in grid and grid[np] != "#" and np not in path:
                if grid[p] not in dl or (grid[p] in dl and dl[grid[p]] == d):
                    if np not in routes or routes[np] < s + 1:
                        path = path + [p]
                        q += [(np, s + 1, path)]
                        routes[np] = s + 1

    return routes[end]


# Is the position a node in our graph? i.e. is start, end or has more than 2
# routes
def is_node(pos, grid):
    count = 0
    for d in [U, D, L, R]:
        np = pos + d
        if np not in grid:
            return True
        elif np in grid and grid[np] != "#":
            count += 1
    return True if count > 2 else False


# Find adjacent nodes and distances from current node
def adjacent_nodes(start, grid):
    q = [(start, 0)]
    seen = set([start])
    nodes = []
    while q:
        p, s = q.pop()
        for d in [U, D, L, R]:
            np = p + d
            if np in grid and grid[np] != "#" and np not in seen:
                seen.add(np)
                if is_node(np, grid):
                    nodes += [(np, s + 1)]
                else:
                    q += [(np, s + 1)]
    return nodes


def part_b(data):
    grid, start, end = parse(data)

    # Build a weighted graph with networkx
    graph = nx.DiGraph()
    seen = set()
    q = [start]
    while q:
        cn = q.pop()
        seen.add(cn)
        for n, d in adjacent_nodes(cn, grid):
            graph.add_edge(cn, n, weight=d)
            if n not in seen:
                q += [n]

    # recover maximum of all simple paths from start to end
    return max(
        path_weight(graph, path, "weight")
        for path in nx.all_simple_paths(graph, start, end)
    )
