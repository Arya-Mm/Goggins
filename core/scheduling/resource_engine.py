def apply_resource_constraint(G, capacity=3):
    timeline = {}

    for node in G.nodes:
        start = G.nodes[node]["ES"]
        end = G.nodes[node]["EF"]
        resource = G.nodes[node]["resource"]

        for t in range(start, end):
            timeline.setdefault(t, 0)
            timeline[t] += resource

            if timeline[t] > capacity:
                # Delay this task by 1 day
                G.nodes[node]["ES"] += 1
                G.nodes[node]["EF"] += 1

    return G