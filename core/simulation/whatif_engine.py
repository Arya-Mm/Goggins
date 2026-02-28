from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk


def run_simulation(
    twin,
    crew_capacity=2,
    productivity_factor=1.0,
    curing_days=2
):

    try:
        # =========================================
        # Generate tasks with modified parameters
        # =========================================
        tasks, dependencies = generate_tasks_from_twin(
            twin,
            productivity_factor=productivity_factor,
            curing_days=curing_days
        )

        G, cycle_valid = build_dependency_graph(tasks, dependencies)

        if not cycle_valid:
            return {"error": "Cycle detected in simulation"}

        # =========================================
        # Run resource-aware scheduling
        # =========================================
        G, critical_path, total_duration = run_cpm(
            G,
            crew_capacity=crew_capacity
        )

        # =========================================
        # Conflict Validation
        # =========================================
        conflicts = detect_conflicts(G, crew_capacity)

        # =========================================
        # Risk
        # =========================================
        risk = calculate_risk(total_duration, len(conflicts))

        return {
            "total_duration": total_duration,
            "critical_path": critical_path,
            "conflicts": conflicts,
            "risk": risk,
            "graph": G  # 🔥 IMPORTANT FIX
        }

    except Exception as e:
        return {"error": str(e)}