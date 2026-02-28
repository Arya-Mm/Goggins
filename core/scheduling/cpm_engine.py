import networkx as nx


def run_cpm(G):

    if not nx.is_directed_acyclic_graph(G):
        raise Exception("Graph contains cycle. Cannot schedule.")

    topo_order = list(nx.topological_sort(G))

    # ======================
    # FORWARD PASS
    # ======================
    for node in topo_order:
        preds = list(G.predecessors(node))

        if not preds:
            ES = 0
        else:
            ES = max(G.nodes[p]["EF"] for p in preds)

        duration = G.nodes[node]["duration"]
        EF = ES + duration

        G.nodes[node]["ES"] = ES
        G.nodes[node]["EF"] = EF

    total_duration = max(G.nodes[n]["EF"] for n in G.nodes)

    # ======================
    # BACKWARD PASS
    # ======================
    for node in reversed(topo_order):
        succs = list(G.successors(node))

        if not succs:
            LF = total_duration
        else:
            LF = min(G.nodes[s]["LS"] for s in succs)

        duration = G.nodes[node]["duration"]
        LS = LF - duration

        G.nodes[node]["LF"] = LF
        G.nodes[node]["LS"] = LS
        G.nodes[node]["slack"] = LS - G.nodes[node]["ES"]

    # ======================
    # CRITICAL PATH
    # ======================
    critical_path = []
    for node in topo_order:
        if G.nodes[node]["slack"] == 0:
            critical_path.append(node)

    return G, critical_path, total_duration