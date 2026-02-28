import networkx as nx


def run_cpm(G):
    if not nx.is_directed_acyclic_graph(G):
        raise Exception("Graph contains cycle. Cannot schedule.")

    topo_order = list(nx.topological_sort(G))

    # ===== FORWARD PASS =====
    for node in topo_order:
        preds = list(G.predecessors(node))
        if not preds:
            G.nodes[node]["ES"] = 0
        else:
            G.nodes[node]["ES"] = max(G.nodes[p]["EF"] for p in preds)

        G.nodes[node]["EF"] = G.nodes[node]["ES"] + G.nodes[node]["duration"]

    total_duration = max(G.nodes[n]["EF"] for n in G.nodes)

    # ===== BACKWARD PASS =====
    for node in reversed(topo_order):
        succs = list(G.successors(node))
        if not succs:
            G.nodes[node]["LF"] = total_duration
        else:
            G.nodes[node]["LF"] = min(G.nodes[s]["LS"] for s in succs)

        G.nodes[node]["LS"] = G.nodes[node]["LF"] - G.nodes[node]["duration"]
        G.nodes[node]["slack"] = G.nodes[node]["LS"] - G.nodes[node]["ES"]

    critical_path = [
        n for n in topo_order if G.nodes[n]["slack"] == 0
    ]

    return G, critical_path, total_duration