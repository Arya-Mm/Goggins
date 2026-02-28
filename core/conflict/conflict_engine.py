def detect_conflicts(G, crew_capacity=2):
    conflicts = []
    timeline = {}

    for node in G.nodes:
        start = G.nodes[node]["ES"]
        end = G.nodes[node]["EF"]
        resource = G.nodes[node]["resource"]

        for t in range(start, end):
            timeline.setdefault(t, 0)
            timeline[t] += resource

            if timeline[t] > crew_capacity:
                conflicts.append({
                    "time": t,
                    "issue": "Crew overload"
                })

    return conflicts