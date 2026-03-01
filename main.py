from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.cpm_engine import run_cpm
from core.conflict.conflict_engine import detect_conflicts
from core.risk.risk_engine import calculate_risk
from core.buildability.buildability_engine import calculate_buildability
from core.utils.heat_visualizer import classify_heat
from core.ai.buildability_explainer import explain_buildability
from core.quantity.quantity_engine import calculate_quantities
from core.vision.scale_calibration import calibrate_scale

from pathlib import Path


# ==========================================================
# STRUCTURAAI CORE ENGINE (DASHBOARD SCHEMA OUTPUT)
# ==========================================================

def run_engine(
    strategy="Balanced",
    crew_capacity=2,
    productivity_factor=1.0,
    curing_days=2,
    demo_pdf_path="core/vision/house_plan.pdf"
):
    """
    Returns dashboard-ready schema for Streamlit UI.
    """

    # ─────────────────────────────────────────
    # STRATEGY MODIFIERS
    # ─────────────────────────────────────────
    if strategy == "FastTrack":
        crew_capacity = max(crew_capacity, 4)
        productivity_factor = max(productivity_factor, 1.2)
        curing_days = max(1, curing_days - 1)

    elif strategy == "CostOptimized":
        crew_capacity = min(crew_capacity, 1)
        productivity_factor = min(productivity_factor, 0.85)

    # ─────────────────────────────────────────
    # VISION
    # ─────────────────────────────────────────
    demo_pdf = Path(demo_pdf_path)

    vision = VisionEngine()
    vision_output = vision.run(str(demo_pdf))

    detection_confidence = vision_output.get("confidence", 0.95)

    # ─────────────────────────────────────────
    # TWIN
    # ─────────────────────────────────────────
    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    # ─────────────────────────────────────────
    # SCALE CALIBRATION
    # ─────────────────────────────────────────
    scale_info = calibrate_scale([
        {"pixel_length": 240, "real_length_inches": 144}
    ])

    # ─────────────────────────────────────────
    # QUANTITIES & COST
    # ─────────────────────────────────────────
    quantities = calculate_quantities(twin)

    quantity_takeoff = quantities.get("material_quantities", [])
    cost_estimation = quantities.get("cost_breakdown", {})

    # ─────────────────────────────────────────
    # TASK & GRAPH
    # ─────────────────────────────────────────
    tasks, dependencies = generate_tasks_from_twin(
        twin,
        productivity_factor=productivity_factor,
        curing_days=curing_days,
        crew_capacity=crew_capacity
    )

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    if not cycle_valid:
        return {"error": "Dependency cycle detected in graph."}

    G, critical_path, total_duration = run_cpm(G, crew_capacity=crew_capacity)

    # ─────────────────────────────────────────
    # CONFLICTS
    # ─────────────────────────────────────────
    conflicts = detect_conflicts(G, crew_capacity=crew_capacity)

    # ─────────────────────────────────────────
    # RISK
    # ─────────────────────────────────────────
    risk = calculate_risk(
        total_duration=total_duration,
        conflicts=conflicts,
        G=G,
        twin=twin,
        critical_path=critical_path
    )

    risk_score = risk.get("risk_score", 3)
    risk_matrix = risk.get("phase_risk", [])

    # ─────────────────────────────────────────
    # BUILDABILITY
    # ─────────────────────────────────────────
    buildability = calculate_buildability(
        G,
        total_duration,
        conflicts,
        risk_data=risk
    )

    build_score = buildability.get("final_score", 80)

    # ─────────────────────────────────────────
    # AI EXPLANATION
    # ─────────────────────────────────────────
    try:
        ai_text = explain_buildability(buildability)
    except Exception:
        ai_text = "AI explanation unavailable."

    # ─────────────────────────────────────────
    # SCHEDULE FORMAT
    # ─────────────────────────────────────────
    schedule = []
    for node in G.nodes():
        node_data = G.nodes[node]
        if "start" in node_data and "finish" in node_data:
            schedule.append({
                "task": node,
                "start": str(node_data["start"]),
                "finish": str(node_data["finish"])
            })

    # ─────────────────────────────────────────
    # DEPENDENCY GRAPH FORMAT
    # ─────────────────────────────────────────
    dependency_graph = {
        "nodes": list(G.nodes()),
        "edges": list(G.edges())
    }

    # ─────────────────────────────────────────
    # PHASE BREAKDOWN (basic version)
    # ─────────────────────────────────────────
    phase_breakdown = []
    for node in G.nodes():
        phase_breakdown.append({
            "phase": node,
            "duration_days": G.nodes[node].get("duration", 0),
            "cost": 0,
            "key_outputs": "Generated by scheduling engine"
        })

    # ─────────────────────────────────────────
    # FINAL DASHBOARD SCHEMA
    # ─────────────────────────────────────────
    dashboard_state = {

        "detection_confidence": detection_confidence,

        "digital_twin": twin,

        "cost_estimation": cost_estimation,

        "quantity_takeoff": quantity_takeoff,

        "schedule": schedule,

        "dependency_graph": dependency_graph,

        "risk_matrix": risk_matrix,

        "conflicts": conflicts,

        "phase_breakdown": phase_breakdown,

        "execution_strategies": {
            strategy: {
                "buildability_score": build_score,
                "duration_days": total_duration
            }
        },

        "strategy_selected": strategy,

        "what_if_parameters": {
            "labor_available": crew_capacity,
            "material_delay_days": 0,
            "budget_factor": 1.0
        },

        "ai_explanation": {
            "summary": ai_text,
            "risk_reasoning": ai_text,
            "recommendation": ai_text
        }
    }

    return dashboard_state