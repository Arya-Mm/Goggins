import networkx as nx


def run_cpm(G, crew_capacity=None):

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
    # RESOURCE LEVELING
    # ======================
    if crew_capacity is not None:
        G = apply_resource_leveling(G, crew_capacity)
        return run_cpm(G, crew_capacity=None)

    # ======================
    # CRITICAL PATH
    # ======================
    critical_path = []
    for node in topo_order:
        if G.nodes[node]["slack"] == 0:
            critical_path.append(node)

    return G, critical_path, total_duration


def apply_resource_leveling(G, crew_capacity):

    timeline = build_timeline(G)

    for time, active_tasks in timeline.items():

        if len(active_tasks) > crew_capacity:

            overload = len(active_tasks) - crew_capacity

            # Sort by highest slack first (delay least critical first)
            active_tasks_sorted = sorted(
                active_tasks,
                key=lambda n: (G.nodes[n]["slack"], G.nodes[n]["ES"]),
                reverse=True
            )

            for i in range(overload):
                task_to_delay = active_tasks_sorted[i]
                delay_task(G, task_to_delay, 1)

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


def delay_task(G, node, delay):

    G.nodes[node]["ES"] += delay
    G.nodes[node]["EF"] += delay

    # Propagate to successors
    for succ in G.successors(node):
        if G.nodes[succ]["ES"] < G.nodes[node]["EF"]:
            shift = G.nodes[node]["EF"] - G.nodes[succ]["ES"]
            delay_task(G, succ, shift)