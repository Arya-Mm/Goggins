from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk

from pathlib import Path


def run_demo():
    print("Running StructuraAI Vision + Twin Demo...")

    demo_pdf = Path("core/vision/house_plan.pdf")

    # =====================
    # VISION
    # =====================
    vision = VisionEngine()
    vision_output = vision.run(str(demo_pdf))

    # =====================
    # TWIN
    # =====================
    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    print("\nDigital Structural Twin:")
    print(twin)

    # =====================
    # DEPENDENCY + CPM
    # =====================
    print("\n--- Dependency & Scheduling Layer ---")

    tasks, dependencies = generate_tasks_from_twin(twin)

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    print("Dependency Graph Valid:", cycle_valid)

    if not cycle_valid:
        print("Cycle detected. Scheduling aborted.")
        return

    G, critical_path, total_duration = run_cpm(G)

    print("\nTotal Project Duration:", total_duration)
    print("Critical Path:", critical_path)

    print("\nTask Schedule:")
    for node in G.nodes:
        print({
            "task": node,
            "ES": G.nodes[node]["ES"],
            "EF": G.nodes[node]["EF"],
            "Slack": G.nodes[node]["slack"]
        })

    # =====================
    # CONFLICT DETECTION
    # =====================
    print("\n--- Conflict Detection ---")

    conflicts = detect_conflicts(G, crew_capacity=2)

    if conflicts:
        print("Conflicts Detected:")
        for conflict in conflicts:
            print(conflict)
    else:
        print("No Conflicts Detected")

    # =====================
    # RISK ASSESSMENT
    # =====================
    print("\n--- Risk Assessment ---")

    risk = calculate_risk(total_duration, len(conflicts))

    print("Risk Score:", risk["risk_score"])
    print("Risk Level:", risk["risk_level"])


if __name__ == "__main__":
    run_demo()