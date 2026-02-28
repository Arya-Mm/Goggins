from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
from core.simulation.whatif_engine import run_simulation
from core.buildability.buildability_engine import calculate_buildability
from core.utils.heat_visualizer import classify_heat
from core.ai.buildability_explainer import explain_buildability
from core.exports.executive_summary import generate_executive_summary
from core.quantity.quantity_engine import calculate_quantities
from core.vision.scale_calibration import calibrate_scale
from core.visualization.gantt_chart import generate_gantt_chart
from core.exports.pdf_report import generate_pdf_report

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
        # =====================
    # STRESS TEST: EMPTY DRAWING
    # =====================
    STRESS_EMPTY = True   # change to False after test

    if STRESS_EMPTY:
        twin = {
            "walls": [],
            "doors": [],
            "windows": [],
            "columns": [],
            "beams": [],
            "slabs": [],
            "summary": {}
        }
    print("\nDigital Structural Twin:")
    print(twin)

    # =====================
    # SCALE CALIBRATION
    # =====================
    print("\n================ SCALE CALIBRATION ================")

    detected_dimensions = [
        {
            "pixel_length": 240,
            "real_length_inches": 144
        }
    ]

    scale_info = calibrate_scale(detected_dimensions)

    print("Pixels per Inch:", scale_info["pixels_per_inch"])
    print("Calibration Status:", scale_info["calibration_status"])

    # =====================
    # QUANTITY & COST ENGINE
    # =====================
    print("\n================ QUANTITY & COST ESTIMATION ================")

    quantities = calculate_quantities(twin)

    print("\n--- Material Quantities ---")
    for k, v in quantities["material_quantities"].items():
        print(f"{k}: {v}")

    print("\n--- Cost Breakdown (₹) ---")
    for k, v in quantities["cost_breakdown"].items():
        print(f"{k}: ₹{v}")

    print("\n--- Phase Breakdown ---")
    for phase, data in quantities["phase_breakdown"].items():
        print(f"\n{phase.upper()}")
        for k, v in data.items():
            print(f"{k}: {v}")

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

    # Generate Gantt Chart
    print("\nGenerating Gantt Chart...")
    gantt_path = generate_gantt_chart(G)
    print("Gantt Chart Saved:", gantt_path)

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

    risk_emoji, _, risk_label = classify_heat(
        risk["risk_score"],
        inverse=True
    )

    print(f"Risk Score: {risk['risk_score']} {risk_emoji}")
    print(f"Risk Level: {risk_label}")
    print("Risk Breakdown:", risk["breakdown"])

    # =====================
    # BUILDABILITY
    # =====================
    print("\n--- Buildability Assessment ---")

    buildability = calculate_buildability(
        G,
        total_duration,
        conflicts,
        risk_data=risk
    )

    build_emoji, _, build_label = classify_heat(
        buildability["final_score"],
        inverse=False
    )

    print(f"Buildability Score: {buildability['final_score']} {build_emoji}")
    print(f"Buildability Level: {build_label}")

    print("\nBuildability Breakdown:")
    for k, v in buildability.items():
        if k not in ["critical_path"]:
            print(f"{k}: {v}")

    # =====================
    # AI JUSTIFICATION
    # =====================
    print("\n--- AI Engineering Justification ---")

    try:
        ai_explanation = explain_buildability(buildability)
        print(ai_explanation)
    except Exception as e:
        print("AI Explanation Failed:", e)

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

    scenario_risk_emoji, _, scenario_risk_label = classify_heat(
        scenario_risk["risk_score"],
        inverse=True
    )

    scenario_build_emoji, _, scenario_build_label = classify_heat(
        scenario_buildability["final_score"],
        inverse=False
    )

    print("\n--- Scenario Comparison ---")

    print("Baseline Duration:", total_duration)
    print("Scenario Duration:", scenario["total_duration"])

    print(f"Baseline Risk: {risk_label}")
    print(f"Scenario Risk: {scenario_risk_label} {scenario_risk_emoji}")

    print(f"Baseline Buildability: {build_label}")
    print(f"Scenario Buildability: {scenario_build_label} {scenario_build_emoji}")

    # =====================
    # PDF EXPORT
    # =====================
    print("\nGenerating PDF Report...")

    pdf_data = {
        "Material Quantities": quantities["material_quantities"],
        "Cost Breakdown": quantities["cost_breakdown"],
        "Risk Summary": risk,
        "Buildability Summary": buildability,
        "Schedule Summary": {
            "Total Duration": total_duration,
            "Critical Path": critical_path
        }
    }

    pdf_path = generate_pdf_report(pdf_data)
    print("PDF Report Saved:", pdf_path)

    # =====================
    # EXECUTIVE SUMMARY
    # =====================
    print("\n================ EXECUTIVE INTELLIGENCE SUMMARY ================")

    summary = generate_executive_summary(
        total_duration,
        scenario["total_duration"],
        risk_label,
        scenario_risk_label,
        build_label,
        scenario_build_label
    )

    print(summary)


if __name__ == "__main__":
    run_demo()