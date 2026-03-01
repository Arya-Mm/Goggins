from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
from core.buildability.buildability_engine import calculate_buildability
from core.utils.heat_visualizer import classify_heat
from core.ai.buildability_explainer import explain_buildability
from core.exports.executive_summary import generate_executive_summary
from core.quantity.quantity_engine import calculate_quantities
from core.vision.scale_calibration import calibrate_scale
from core.visualization.gantt_chart import generate_gantt_chart
from core.exports.pdf_report import generate_pdf_report

from pathlib import Path


# ==========================================================
# CORE ENGINE (Reusable by Streamlit)
# ==========================================================

def run_engine(
    strategy="Balanced",
    crew_capacity=2,
    productivity_factor=1.0,
    curing_days=2,
    demo_pdf_path="core/vision/house_plan.pdf"
):
    """
    strategy:
        - Balanced
        - FastTrack
        - CostOptimized
    """

    # ------------------------------------------------------
    # STRATEGY LOGIC
    # ------------------------------------------------------
    if strategy == "FastTrack":
        crew_capacity = max(crew_capacity, 4)
        productivity_factor = max(productivity_factor, 1.2)
        curing_days = max(1, curing_days - 1)

    elif strategy == "CostOptimized":
        crew_capacity = min(crew_capacity, 1)
        productivity_factor = min(productivity_factor, 0.85)

    # ------------------------------------------------------
    # VISION
    # ------------------------------------------------------
    demo_pdf = Path(demo_pdf_path)

    vision = VisionEngine()
    vision_output = vision.run(str(demo_pdf))

    # ------------------------------------------------------
    # TWIN
    # ------------------------------------------------------
    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    # ------------------------------------------------------
    # SCALE CALIBRATION
    # ------------------------------------------------------
    detected_dimensions = [
        {
            "pixel_length": 240,
            "real_length_inches": 144
        }
    ]

    scale_info = calibrate_scale(detected_dimensions)

    # ------------------------------------------------------
    # QUANTITY & COST
    # ------------------------------------------------------
    quantities = calculate_quantities(twin)

    # ------------------------------------------------------
    # SCHEDULING
    # ------------------------------------------------------
    tasks, dependencies = generate_tasks_from_twin(
        twin,
        productivity_factor=productivity_factor,
        curing_days=curing_days,
        crew_capacity=crew_capacity
    )

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    if not cycle_valid:
        return {"error": "Dependency cycle detected in graph."}

    G, critical_path, total_duration = run_cpm(
        G,
        crew_capacity=crew_capacity
    )

    gantt_path = generate_gantt_chart(G)

    # ------------------------------------------------------
    # CONFLICTS
    # ------------------------------------------------------
    conflicts = detect_conflicts(G, crew_capacity=crew_capacity)

    # ------------------------------------------------------
    # RISK
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # BUILDABILITY
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # AI EXPLANATION
    # ------------------------------------------------------
    try:
        ai_explanation = explain_buildability(buildability)
    except Exception:
        ai_explanation = "AI explanation unavailable."

    # ------------------------------------------------------
    # EXECUTIVE SUMMARY
    # ------------------------------------------------------
    summary = generate_executive_summary(
        total_duration,
        total_duration,
        risk_label,
        risk_label,
        build_label,
        build_label
    )

    # ------------------------------------------------------
    # PDF DATA PACKAGE
    # ------------------------------------------------------
    pdf_data = {
        "Twin Summary": twin.get("summary", {}),
        "Material Quantities": quantities.get("material_quantities", {}),
        "Cost Breakdown": quantities.get("cost_breakdown", {}),
        "Risk Summary": risk,
        "Buildability Summary": buildability,
        "AI Explanation": ai_explanation,
        "Executive Summary": summary
    }

    # DO NOT auto-generate PDF here in engine
    # Let Streamlit trigger it when needed

    return {
        "twin": twin,
        "scale_info": scale_info,
        "quantities": quantities,
        "graph": G,
        "critical_path": critical_path,
        "duration": total_duration,
        "conflicts": conflicts,
        "risk": risk,
        "risk_label": risk_label,
        "risk_emoji": risk_emoji,
        "buildability": buildability,
        "build_label": build_label,
        "build_emoji": build_emoji,
        "ai_explanation": ai_explanation,
        "summary": summary,
        "pdf_data": pdf_data,
        "gantt_path": gantt_path
    }


# ==========================================================
# CLI MODE (python main.py)
# ==========================================================

def run_demo():
    print("Running StructuraAI Vision + Twin Demo...\n")

    result = run_engine(strategy="Balanced")

    if "error" in result:
        print(result["error"])
        return

    print("Digital Structural Twin:")
    print(result["twin"])
    print("\nScale Calibration:", result["scale_info"])

    print("\n================ QUANTITY & COST =================")
    print(result["quantities"])

    print("\n================ EXECUTION =================")
    print("Duration:", result["duration"])
    print("Critical Path:", result["critical_path"])

    print("\nRisk Score:", result["risk"]["risk_score"], result["risk_emoji"])
    print("Risk Level:", result["risk_label"])

    print("\nBuildability Score:", result["buildability"]["final_score"], result["build_emoji"])
    print("Buildability Level:", result["build_label"])

    print("\n================ AI EXPLANATION =================")
    print(result["ai_explanation"])

    print("\n================ EXECUTIVE SUMMARY =================")
    print(result["summary"])


if __name__ == "__main__":
    run_demo()