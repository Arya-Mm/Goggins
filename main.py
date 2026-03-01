import time

from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
from core.buildability.buildability_engine import calculate_buildability
from core.ai.buildability_explainer import explain_buildability
from core.quantity.quantity_engine import calculate_quantities
from core.exports.pdf_report import generate_pdf_report


# ─────────────────────────────────────────────
# STAGE 1 — VISION (IN-MEMORY)
# ─────────────────────────────────────────────
def run_vision_stage(pdf_bytes):

    start = time.time()

    vision = VisionEngine()
    vision_output = vision.run(pdf_bytes)

    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    duration = time.time() - start

    return {
        "twin": twin,
        "confidence": vision_output.get("confidence", 0.95),
        "stage_time": duration
    }


# ─────────────────────────────────────────────
# STAGE 2 — PLANNING
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
def export_pdf(data, filename="StructuraAI_Report.pdf"):
    generate_pdf_report(data, filename)
    return filename