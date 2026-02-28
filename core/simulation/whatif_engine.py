from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk


def run_simulation(twin, crew_capacity=2, productivity_factor=1.0, curing_days=2):

    # Adjust durations dynamically
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

    conflicts = detect_conflicts(G, crew_capacity=crew_capacity)
    risk = calculate_risk(total_duration, len(conflicts))

    return {
        "total_duration": total_duration,
        "critical_path": critical_path,
        "conflicts": conflicts,
        "risk": risk
    }   