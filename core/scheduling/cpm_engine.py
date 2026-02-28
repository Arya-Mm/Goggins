import networkx as nx


def run_cpm(G, crew_capacity=None):

    if not nx.is_directed_acyclic_graph(G):
        raise Exception("Graph contains cycle. Cannot schedule.")

    # Initial CPM computation
    G = compute_cpm(G)

    # Apply resource leveling if capacity defined
    if crew_capacity is not None:
        G = apply_resource_leveling(G, crew_capacity)
        G = compute_cpm(G)  # Recompute after leveling

    total_duration = max(G.nodes[n]["EF"] for n in G.nodes)

    # Critical path
    critical_path = [
        n for n in nx.topological_sort(G)
        if G.nodes[n]["slack"] == 0
    ]

    return G, critical_path, total_duration


# =====================================================
# CPM CALCULATION
# =====================================================

def compute_cpm(G):

    topo_order = list(nx.topological_sort(G))

    # FORWARD PASS
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

    # BACKWARD PASS
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

    return G


# =====================================================
# RESOURCE LEVELING (BATCHING MODEL)
# =====================================================

def apply_resource_leveling(G, crew_capacity):

    timeline = build_timeline(G)

    for time in sorted(timeline.keys()):

        active_tasks = timeline[time]

        if len(active_tasks) > crew_capacity:

            # Deterministic order
            active_tasks_sorted = sorted(
                active_tasks,
                key=lambda n: G.nodes[n]["ES"]
            )

            for i, task in enumerate(active_tasks_sorted):

                batch_index = i // crew_capacity
                new_start = time + batch_index

                if G.nodes[task]["ES"] < new_start:
                    shift = new_start - G.nodes[task]["ES"]
                    delay_task(G, task, shift)

    return G


def build_timeline(G):

    timeline = {}

    for node in G.nodes:
        ES = G.nodes[node]["ES"]
        EF = G.nodes[node]["EF"]

        for t in range(ES, EF):
            if t not in timeline:
                timeline[t] = []
            timeline[t].append(node)

    return timeline


def delay_task(G, node, shift):

    G.nodes[node]["ES"] += shift
    G.nodes[node]["EF"] += shift

    # Propagate shift to successors
    for succ in G.successors(node):
        if G.nodes[succ]["ES"] < G.nodes[node]["EF"]:
            needed_shift = G.nodes[node]["EF"] - G.nodes[succ]["ES"]
            delay_task(G, succ, needed_shift)