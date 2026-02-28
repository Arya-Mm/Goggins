from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
from core.simulation.whatif_engine import run_simulation
from core.buildability.buildability_engine import calculate_buildability

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
    # BASELINE EXECUTION
    # =====================
    print("\n================ BASELINE EXECUTION INTELLIGENCE ================")

    tasks, dependencies = generate_tasks_from_twin(
        twin,
        productivity_factor=1.0,
        curing_days=2,
        crew_capacity=2
    )

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    if not cycle_valid:
        print("Dependency Graph Invalid: ✗ Cycle Detected")
        return

    print("Dependency Graph Valid: ✓ No Cycles")

    G, critical_path, total_duration = run_cpm(G, crew_capacity=2)

    print("\nTotal Project Duration:", total_duration)
    print("Critical Path:", critical_path)

    # =====================
    # CONFLICTS
    # =====================
    print("\n--- Conflict Validation ---")

    conflicts = detect_conflicts(G, crew_capacity=2)

    if conflicts:
        for conflict in conflicts:
            print("⚠", conflict)
    else:
        print("No Conflicts Detected ✓")

    # =====================
    # RISK
    # =====================
    print("\n--- Risk Assessment ---")

    risk = calculate_risk(
        total_duration=total_duration,
        conflicts=conflicts,
        G=G,
        twin=twin,
        critical_path=critical_path
    )

    print("Risk Score:", risk["risk_score"])
    print("Risk Level:", risk["risk_level"])
    print("Risk Breakdown:", risk["breakdown"])

    # =====================
    # BUILDABILITY (UPGRADED)
    # =====================
    print("\n--- Buildability Assessment ---")

    buildability = calculate_buildability(
        G,
        total_duration,
        conflicts,
        risk_data=risk
    )

    print("Buildability Score:", buildability["final_score"])
    print("Buildability Level:", buildability["level"])

    print("\nBuildability Breakdown:")
    for k, v in buildability.items():
        if k not in ["critical_path"]:
            print(f"{k}: {v}")

    # =====================
    # WHAT-IF SIMULATION
    # =====================
    print("\n================ WHAT-IF SIMULATION ================")

    scenario = run_simulation(
        twin,
        crew_capacity=3,
        productivity_factor=1.2,
        curing_days=1
    )

    if "error" in scenario:
        print("Simulation Error:", scenario["error"])
        return

    scenario_risk = calculate_risk(
        total_duration=scenario["total_duration"],
        conflicts=scenario["conflicts"],
        G=scenario["graph"],
        twin=twin,
        critical_path=scenario["critical_path"]
    )

    scenario_buildability = calculate_buildability(
        scenario["graph"],
        scenario["total_duration"],
        scenario["conflicts"],
        risk_data=scenario_risk
    )

    print("\n--- Scenario Comparison ---")
    print("Baseline Duration:", total_duration)
    print("Scenario Duration:", scenario["total_duration"])
    print("Baseline Risk:", risk["risk_level"])
    print("Scenario Risk:", scenario_risk["risk_level"])
    print("Baseline Buildability:", buildability["level"])
    print("Scenario Buildability:", scenario_buildability["level"])


if __name__ == "__main__":
    run_demo()