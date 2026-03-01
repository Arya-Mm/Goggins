# core/scheduling/cpm_engine.py

import networkx as nx


def run_cpm(G, crew_capacity=None):

    # SAFE EXIT
    if G is None or len(G.nodes) == 0:
        return G, [], 0

    if not nx.is_directed_acyclic_graph(G):
        raise Exception("Graph contains cycle. Cannot schedule.")

    # Initial CPM
    G = compute_cpm(G)

    # Resource leveling (non-destructive)
    if crew_capacity is not None and len(G.nodes) > 0:
        G = apply_resource_leveling(G, crew_capacity)
        G = compute_cpm(G)  # Recompute ES/EF/LS/LF after leveling

    total_duration = max(G.nodes[n]["EF"] for n in G.nodes)

    # TRUE critical path using longest path
    critical_path = nx.algorithms.dag.dag_longest_path(G, weight="duration")

    return G, critical_path, total_duration


# =====================================================
# CPM CORE
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

        duration = G.nodes[node].get("duration", 0)

        G.nodes[node]["ES"] = ES
        G.nodes[node]["EF"] = ES + duration

    total_duration = max(G.nodes[n]["EF"] for n in G.nodes)

    # BACKWARD PASS
    for node in reversed(topo_order):

        succs = list(G.successors(node))

        if not succs:
            LF = total_duration
        else:
            LF = min(G.nodes[s]["LS"] for s in succs)

        duration = G.nodes[node].get("duration", 0)

        G.nodes[node]["LF"] = LF
        G.nodes[node]["LS"] = LF - duration
        G.nodes[node]["slack"] = G.nodes[node]["LS"] - G.nodes[node]["ES"]

    return G


# =====================================================
# RESOURCE LEVELING (FLOAT-PRESERVING)
# =====================================================

def apply_resource_leveling(G, crew_capacity):

    timeline = build_timeline(G)

    for time in sorted(timeline.keys()):

        active_tasks = timeline[time]

        if len(active_tasks) > crew_capacity:

            # Sort by earliest start
            active_tasks_sorted = sorted(
                active_tasks,
                key=lambda n: G.nodes[n]["ES"]
            )

            for i, task in enumerate(active_tasks_sorted):

                batch_index = i // crew_capacity
                new_start = time + batch_index

                if G.nodes[task]["ES"] < new_start:
                    shift = new_start - G.nodes[task]["ES"]
                    delay_task_non_recursive(G, task, shift)

    return G


def build_timeline(G):

    timeline = {}

    for node in G.nodes:
        ES = G.nodes[node]["ES"]
        EF = G.nodes[node]["EF"]

        for t in range(ES, EF):
            timeline.setdefault(t, []).append(node)

    return timeline


# =====================================================
# NON-RECURSIVE DELAY (CRITICAL FIX)
# =====================================================

def delay_task_non_recursive(G, node, shift):

    # Shift only this node
    G.nodes[node]["ES"] += shift
    G.nodes[node]["EF"] += shift

    # Only ensure precedence validity
    for succ in G.successors(node):

        if G.nodes[succ]["ES"] < G.nodes[node]["EF"]:
            required_shift = G.nodes[node]["EF"] - G.nodes[succ]["ES"]

            G.nodes[succ]["ES"] += required_shift
            G.nodes[succ]["EF"] += required_shift