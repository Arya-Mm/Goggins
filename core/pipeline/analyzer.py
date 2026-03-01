# core/pipeline/analyzer.py

from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
from core.buildability.buildability_engine import calculate_buildability
from core.quantity.quantity_engine import calculate_quantities
from core.vision.scale_calibration import calibrate_scale
from core.visualization.gantt_chart import generate_gantt_chart
from core.exports.pdf_report import generate_pdf_report


def analyze_project(pdf_path, stress_config=None):

    stress_config = stress_config or {}

    # ======================
    # Vision
    # ======================
    vision = VisionEngine()
    vision_output = vision.run(str(pdf_path))

    # ======================
    # Twin
    # ======================
    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    # ======================
    # Scale Calibration (FIXED)
    # ======================
    scale_info = calibrate_scale(vision_output.get("dimensions", []))

    # ======================
    # Quantity
    # ======================
    quantities = calculate_quantities(twin)

    # ======================
    # Scheduling
    # ======================
    tasks, dependencies = generate_tasks_from_twin(
        twin,
        productivity_factor=1.0,
        curing_days=2,
        crew_capacity=2
    )

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    if not cycle_valid:
        return {"error": "Dependency cycle detected"}

    G, critical_path, total_duration = run_cpm(G, crew_capacity=2)

    conflicts = detect_conflicts(G, crew_capacity=2)

    # ======================
    # Risk
    # ======================
    risk = calculate_risk(
        total_duration=total_duration,
        conflicts=conflicts,
        G=G,
        twin=twin,
        critical_path=critical_path
    )

    # ======================
    # Buildability
    # ======================
    buildability = calculate_buildability(
        G,
        total_duration,
        conflicts,
        risk_data=risk
    )

    # ======================
    # Visualization
    # ======================
    gantt_path = generate_gantt_chart(G)

    # ======================
    # PDF Export
    # ======================
    pdf_data = {
        "Material Quantities": quantities["material_quantities"],
        "Cost Breakdown": quantities["cost_breakdown"],
        "Risk Summary": risk,
        "Buildability Summary": buildability,
        "Duration": total_duration
    }

    pdf_path = generate_pdf_report(pdf_data)

    # ======================
    # Final Structured Output
    # ======================
    return {
        "twin": twin,
        "scale": scale_info,
        "quantities": quantities,
        "risk": risk,
        "buildability": buildability,
        "schedule": {
            "total_duration": total_duration,
            "critical_path": critical_path,
            "graph": G
        },
        "gantt_path": gantt_path,
        "pdf_path": pdf_path
    }