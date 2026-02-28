import networkx as nx


def run_cpm(G, crew_capacity=None):

    # ✅ EMPTY GRAPH SAFE EXIT
    if G is None or len(G.nodes) == 0:
        return G, [], 0

    if not nx.is_directed_acyclic_graph(G):
        raise Exception("Graph contains cycle. Cannot schedule.")

    # Initial CPM computation
    G = compute_cpm(G)

    # Apply resource leveling if capacity defined
    if crew_capacity is not None and len(G.nodes) > 0:
        G = apply_resource_leveling(G, crew_capacity)
        G = compute_cpm(G)  # Recompute after leveling

    # ✅ SAFE total_duration
    if len(G.nodes) == 0:
        total_duration = 0
    else:
        total_duration = max(
            G.nodes[n].get("EF", 0) for n in G.nodes
        )

    # Critical path (safe)
    critical_path = [
        n for n in nx.topological_sort(G)
        if G.nodes[n].get("slack", 0) == 0
    ] if len(G.nodes) > 0 else []

    return G, critical_path, total_duration


# =====================================================
# CPM CALCULATION
# =====================================================

def compute_cpm(G):

    # ✅ EMPTY SAFE
    if len(G.nodes) == 0:
        return G

    topo_order = list(nx.topological_sort(G))

    # FORWARD PASS
    for node in topo_order:

        preds = list(G.predecessors(node))

        if not preds:
            ES = 0
        else:
            ES = max(G.nodes[p].get("EF", 0) for p in preds)

        duration = G.nodes[node].get("duration", 0)
        EF = ES + duration

        G.nodes[node]["ES"] = ES
        G.nodes[node]["EF"] = EF

    # SAFE total duration
    total_duration = max(
        G.nodes[n].get("EF", 0) for n in G.nodes
    ) if len(G.nodes) > 0 else 0

    # BACKWARD PASS
    for node in reversed(topo_order):

        succs = list(G.successors(node))

        if not succs:
            LF = total_duration
        else:
            LF = min(G.nodes[s].get("LS", total_duration) for s in succs)

        duration = G.nodes[node].get("duration", 0)
        LS = LF - duration

        G.nodes[node]["LF"] = LF
        G.nodes[node]["LS"] = LS
        G.nodes[node]["slack"] = LS - G.nodes[node].get("ES", 0)

    return G


# =====================================================
# RESOURCE LEVELING (BATCHING MODEL)
# =====================================================

def apply_resource_leveling(G, crew_capacity):

    if len(G.nodes) == 0:
        return G

    timeline = build_timeline(G)

    for time in sorted(timeline.keys()):

        active_tasks = timeline[time]

        if len(active_tasks) > crew_capacity:

            active_tasks_sorted = sorted(
                active_tasks,
                key=lambda n: G.nodes[n].get("ES", 0)
            )

            for i, task in enumerate(active_tasks_sorted):

                batch_index = i // crew_capacity
                new_start = time + batch_index

                if G.nodes[task].get("ES", 0) < new_start:
                    shift = new_start - G.nodes[task]["ES"]
                    delay_task(G, task, shift)

    return G


def build_timeline(G):

    timeline = {}

    for node in G.nodes:
        ES = G.nodes[node].get("ES", 0)
        EF = G.nodes[node].get("EF", 0)

        for t in range(ES, EF):
            if t not in timeline:
                timeline[t] = []
            timeline[t].append(node)

    return timeline


def delay_task(G, node, shift):

    G.nodes[node]["ES"] += shift
    G.nodes[node]["EF"] += shift

    # Propagate shift safely
    for succ in G.successors(node):
        if G.nodes[succ].get("ES", 0) < G.nodes[node]["EF"]:
            needed_shift = G.nodes[node]["EF"] - G.nodes[succ]["ES"]
            delay_task(G, succ, needed_shift)