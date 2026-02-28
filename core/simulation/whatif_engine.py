from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
import networkx as nx


def level_resources(G, crew_capacity):

    # Sort tasks by earliest start
    tasks = sorted(G.nodes, key=lambda n: G.nodes[n]["ES"])

    timeline = {}

    for node in tasks:
        start = G.nodes[node]["ES"]
        duration = G.nodes[node]["duration"]
        resource = G.nodes[node]["resource"]

        while True:
            overload = False

            for t in range(start, start + duration):
                timeline.setdefault(t, 0)
                if timeline[t] + resource > crew_capacity:
                    overload = True
                    break

            if overload:
                start += 1
            else:
                break

        # Update schedule
        G.nodes[node]["ES"] = start
        G.nodes[node]["EF"] = start + duration

        for t in range(start, start + duration):
            timeline[t] += resource

    return G


def run_simulation(twin, crew_capacity=2, productivity_factor=1.0, curing_days=2):

    tasks, dependencies = generate_tasks_from_twin(twin)

    for task in tasks:
        if task["type"] == "wall_build":
            task["duration"] = max(1, int(task["duration"] / productivity_factor))
        if task["type"] == "wall_cure":
            task["duration"] = curing_days

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    if not cycle_valid:
        return {"error": "Cycle detected"}

    G, critical_path, total_duration = run_cpm(G)

    # 🔥 NEW: Resource leveling
    G = level_resources(G, crew_capacity)

    # Recalculate total duration after leveling
    total_duration = max(G.nodes[n]["EF"] for n in G.nodes)

    conflicts = detect_conflicts(G, crew_capacity=crew_capacity)
    risk = calculate_risk(total_duration, len(conflicts))

    return {
        "total_duration": total_duration,
        "critical_path": critical_path,
        "conflicts": conflicts,
        "risk": risk
    }