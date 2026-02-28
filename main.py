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

    tasks, dependencies = generate_tasks_from_twin(twin)
    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    if cycle_valid:
        print("\nDependency Graph Valid: ✓ No Cycles")
    else:
        print("\nDependency Graph Invalid: ✗ Cycle Detected")
        return

    # RESOURCE-AWARE SCHEDULING
    G, critical_path, total_duration = run_cpm(G, crew_capacity=2)

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
    # CONFLICT VALIDATION
    # =====================
    print("\n--- Conflict Validation ---")

    conflicts = detect_conflicts(G, crew_capacity=2)

    if conflicts:
        print("Conflicts Detected:")
        for conflict in conflicts:
            print(conflict)
    else:
        print("No Conflicts Detected ✓")

    # =====================
    # RISK ASSESSMENT (UPGRADED)
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
    # BUILDABILITY SCORE
    # =====================
    print("\n--- Buildability Assessment ---")

    buildability = calculate_buildability(G, total_duration, conflicts)

    print("Buildability Score:", buildability["buildability_score"])
    print("Buildability Level:", buildability["buildability_level"])

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

    print("\nScenario: Increased Crew + Faster Build + Shorter Cure")
    print("New Total Duration:", scenario["total_duration"])
    print("New Critical Path:", scenario["critical_path"])

    if scenario["conflicts"]:
        print("New Conflicts:")
        for conflict in scenario["conflicts"]:
            print(conflict)
    else:
        print("No Conflicts in Scenario ✓")

    # 🔥 Scenario Risk Using Upgraded Engine
    scenario_risk = calculate_risk(
        total_duration=scenario["total_duration"],
        conflicts=scenario["conflicts"],
        G=scenario["graph"],
        twin=twin,
        critical_path=scenario["critical_path"]
    )

    print("New Risk Score:", scenario_risk["risk_score"])
    print("New Risk Level:", scenario_risk["risk_level"])
    print("Scenario Risk Breakdown:", scenario_risk["breakdown"])

    # Scenario Buildability
    scenario_buildability = calculate_buildability(
        scenario["graph"],
        scenario["total_duration"],
        scenario["conflicts"]
    )

    print("Scenario Buildability Score:", scenario_buildability["buildability_score"])
    print("Scenario Buildability Level:", scenario_buildability["buildability_level"])

    # =====================
    # EXECUTIVE SUMMARY
    # =====================
    print("\n================ EXECUTIVE INTELLIGENCE SUMMARY ================")

    print("Baseline Duration:", total_duration)
    print("Scenario Duration:", scenario["total_duration"])
    print("Baseline Risk:", risk["risk_level"])
    print("Scenario Risk:", scenario_risk["risk_level"])
    print("Baseline Buildability:", buildability["buildability_level"])
    print("Scenario Buildability:", scenario_buildability["buildability_level"])


if __name__ == "__main__":
    run_demo()