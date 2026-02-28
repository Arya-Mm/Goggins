def detect_conflicts(G, crew_capacity=2):
    timeline = {}
    overload_times = set()

    # Build resource timeline
    for node in G.nodes:
        start = G.nodes[node]["ES"]
        end = G.nodes[node]["EF"]
        resource = G.nodes[node]["resource"]

        for t in range(start, end):
            timeline.setdefault(t, 0)
            timeline[t] += resource

    # Detect overload
    for t, load in timeline.items():
        if load > crew_capacity:
            overload_times.add(t)

    conflicts = []
    for t in sorted(overload_times):
        conflicts.append({
            "time": t,
            "total_load": timeline[t],
            "capacity": crew_capacity,
            "issue": "Crew overload"
        })

    return conflicts