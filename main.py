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

    # ======================================================
    # STRESS TEST CONTROL PANEL
    # Toggle True / False only here
    # ======================================================

    STRESS_EMPTY_TWIN = True
    STRESS_NO_DIMENSION = True
    STRESS_HIGH_UNCERTAINTY = True
    STRESS_NO_WALLS = True
    STRESS_FORCE_CYCLE = True
    STRESS_ZERO_DURATION = True
    STRESS_MAX_RISK = True

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

    # 🔥 STRESS: EMPTY TWIN
    if STRESS_EMPTY_TWIN:
        twin = {
            "walls": [],
            "doors": [],
            "windows": [],
            "columns": [],
            "beams": [],
            "slabs": [],
            "summary": {}
        }

    # 🔥 STRESS: HIGH UNCERTAINTY
    if STRESS_HIGH_UNCERTAINTY and twin.get("walls"):
        twin["walls"][0]["dimension_uncertain"] = True
        twin["confidence_score"] = 20

    # 🔥 STRESS: REMOVE WALLS
    if STRESS_NO_WALLS:
        twin["walls"] = []

    print("\nDigital Structural Twin:")
    print(twin)

    # =====================
    # SCALE CALIBRATION
    # =====================
    print("\n================ SCALE CALIBRATION ================")

    if STRESS_NO_DIMENSION:
        detected_dimensions = []
    else:
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
    # QUANTITY ENGINE
    # =====================
    print("\n================ QUANTITY & COST ESTIMATION ================")

    quantities = calculate_quantities(twin)

    print("\n--- Material Quantities ---")
    for k, v in quantities["material_quantities"].items():
        print(f"{k}: {v}")

    print("\n--- Cost Breakdown (₹) ---")
    for k, v in quantities["cost_breakdown"].items():
        print(f"{k}: ₹{v}")

    # =====================
    # SCHEDULING
    # =====================
    print("\n================ BASELINE EXECUTION INTELLIGENCE ================")

    tasks, dependencies = generate_tasks_from_twin(
        twin,
        productivity_factor=1.0,
        curing_days=2,
        crew_capacity=2
    )

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    # 🔥 STRESS: FORCE CYCLE
    if STRESS_FORCE_CYCLE and len(G.nodes) > 1:
        nodes = list(G.nodes)
        G.add_edge(nodes[-1], nodes[0])

    if not cycle_valid:
        print("Dependency Graph Invalid: ✗ Cycle Detected")
        return

    print("Dependency Graph Valid: ✓ No Cycles")

    G, critical_path, total_duration = run_cpm(G, crew_capacity=2)

    # 🔥 STRESS: ZERO DURATION
    if STRESS_ZERO_DURATION and len(G.nodes) > 0:
        node = list(G.nodes)[0]
        G.nodes[node]["EF"] = G.nodes[node]["ES"]

    print("\nTotal Project Duration:", total_duration)
    print("Critical Path:", critical_path)

    print("\nGenerating Gantt Chart...")
    gantt_path = generate_gantt_chart(G)
    print("Gantt Chart Saved:", gantt_path)

    # =====================
    # CONFLICTS
    # =====================
    conflicts = detect_conflicts(G, crew_capacity=2)

    # =====================
    # RISK
    # =====================
    risk = calculate_risk(
        total_duration=total_duration,
        conflicts=conflicts,
        G=G,
        twin=twin,
        critical_path=critical_path
    )

    # 🔥 STRESS: MAX RISK
    if STRESS_MAX_RISK:
        risk["risk_score"] = 100

    risk_emoji, _, risk_label = classify_heat(
        risk["risk_score"],
        inverse=True
    )

    print("\nRisk Score:", risk["risk_score"], risk_emoji)
    print("Risk Level:", risk_label)

    # =====================
    # BUILDABILITY
    # =====================
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

    print("\nBuildability Score:", buildability["final_score"], build_emoji)
    print("Buildability Level:", build_label)

    # =====================
    # AI EXPLANATION
    # =====================
    try:
        ai_explanation = explain_buildability(buildability)
        print("\nAI Explanation:")
        print(ai_explanation)
    except Exception as e:
        print("AI Explanation Failed:", e)

    # =====================
    # PDF EXPORT
    # =====================
    pdf_data = {
        "Material Quantities": quantities["material_quantities"],
        "Cost Breakdown": quantities["cost_breakdown"],
        "Risk Summary": risk,
        "Buildability Summary": buildability,
    }

    pdf_path = generate_pdf_report(pdf_data)
    print("\nPDF Report Saved:", pdf_path)

    # =====================
    # EXECUTIVE SUMMARY
    # =====================
    summary = generate_executive_summary(
        total_duration,
        total_duration,
        risk_label,
        risk_label,
        build_label,
        build_label
    )

    print("\n================ EXECUTIVE SUMMARY ================")
    print(summary)


if __name__ == "__main__":
    run_demo()