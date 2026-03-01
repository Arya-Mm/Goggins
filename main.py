import time
from pathlib import Path

from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
from core.buildability.buildability_engine import calculate_buildability
from core.ai.buildability_explainer import explain_buildability
from core.quantity.quantity_engine import calculate_quantities
from core.vision.scale_calibration import calibrate_scale
from core.exports.pdf_report import generate_pdf_report


# ─────────────────────────────────────────────
# STAGE 1 — VISION + TWIN (Heavy)
# ─────────────────────────────────────────────
def run_vision_stage(file_path):

    start = time.time()

    vision = VisionEngine()
    vision_output = vision.run(str(file_path))

    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    scale = calibrate_scale([
        {"pixel_length": 240, "real_length_inches": 144}
    ])

    duration = time.time() - start

    return {
        "twin": twin,
        "scale_info": scale,
        "confidence": vision_output.get("confidence", 0.95),
        "stage_time": duration
    }


# ─────────────────────────────────────────────
# STAGE 2 — SCHEDULING + INTELLIGENCE
# ─────────────────────────────────────────────
def run_planning_stage(twin, strategy, crew, productivity, curing):

    start = time.time()

    quantities = calculate_quantities(twin)

    tasks, deps = generate_tasks_from_twin(
        twin,
        productivity_factor=productivity,
        curing_days=curing,
        crew_capacity=crew
    )

    G, valid = build_dependency_graph(tasks, deps)
    if not valid:
        return {"error": "Dependency cycle detected"}

    G, critical_path, total_duration = run_cpm(G, crew_capacity=crew)

    conflicts = detect_conflicts(G, crew_capacity=crew)

    risk = calculate_risk(
        total_duration=total_duration,
        conflicts=conflicts,
        G=G,
        twin=twin,
        critical_path=critical_path
    )

    buildability = calculate_buildability(
        G,
        total_duration,
        conflicts,
        risk_data=risk
    )

    try:
        ai_text = explain_buildability(buildability)
    except:
        ai_text = "AI explanation unavailable."

    duration = time.time() - start

    return {
        "quantities": quantities,
        "graph": G,
        "duration": total_duration,
        "conflicts": conflicts,
        "risk": risk,
        "buildability": buildability,
        "ai_text": ai_text,
        "stage_time": duration
    }


# ─────────────────────────────────────────────
# PDF EXPORT
# ─────────────────────────────────────────────
def export_pdf(data, output_path="report.pdf"):
    generate_pdf_report(data, output_path)
    return output_path