import networkx as nx


# networkx to the rescue...
def part_a(data):
    g = nx.Graph()
    for line in data.splitlines():
        fr, to = line.split(": ")
        for t in to.split(" "):
            g.add_edge(fr, t)

    g.remove_edges_from(nx.minimum_edge_cut(g))
    c1, c2 = nx.connected_components(g)
    return len(c1) * len(c2)
