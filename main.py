import os
import json
import streamlit as st
from datetime import datetime

# ===== MODULE IMPORTS (Will exist soon) =====
from ingestion.loader import load_blueprint
from vision.detector import detect_structural_elements
from vision.wall_hough import detect_walls
from vision.ocr import extract_dimensions
from twin.scale import calibrate_scale
from twin.builder import build_structural_twin
from twin.takeoff import compute_quantities
from graph.dependency import build_dependency_graph
from scheduling.planner import generate_schedule
from conflict.checker import detect_conflicts
from risk.simulator import simulate_risk
from optimization.buildability import compute_buildability_score
from ai.explainer import generate_explanation


# =====================================================
# CONFIGURATION
# =====================================================

PROJECT_STATE_FILE = "project_state.json"
DETECTED_STRUCTURE_FILE = "detected_structure.json"


# =====================================================
# STREAMLIT UI
# =====================================================

st.set_page_config(page_title="StructuraAI", layout="wide")
st.title("STRUCTURAAI — Autonomous Pre-Construction Intelligence Engine")

uploaded_file = st.file_uploader("Upload Blueprint (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])


# =====================================================
# PIPELINE EXECUTION
# =====================================================

def run_pipeline(file):
    project_state = {
        "timestamp": str(datetime.now()),
        "status": "Running",
        "confidence_overall": 1.0
    }

    # 1️⃣ Blueprint Ingestion
    blueprint = load_blueprint(file)

    # 2️⃣ Structural Detection
    detections = detect_structural_elements(blueprint)

    # 3️⃣ Wall Detection
    walls = detect_walls(blueprint)

    # 4️⃣ OCR Dimension Extraction
    dimensions = extract_dimensions(blueprint)

    # 5️⃣ Scale Calibration
    scale_factor, scale_confidence = calibrate_scale(dimensions)

    # 6️⃣ Digital Structural Twin
    structural_twin = build_structural_twin(
        detections,
        walls,
        dimensions,
        scale_factor
    )

    # Save detected structure
    with open(DETECTED_STRUCTURE_FILE, "w") as f:
        json.dump(structural_twin, f, indent=4)

    # 7️⃣ Quantity Takeoff
    quantities = compute_quantities(structural_twin)

    # 8️⃣ Dependency Graph
    dependency_graph = build_dependency_graph(structural_twin)

    # 9️⃣ Scheduling Engine
    schedule = generate_schedule(dependency_graph, strategy="Balanced")

    # 🔟 Conflict Detection
    conflicts = detect_conflicts(schedule)

    # 1️⃣1️⃣ Risk Simulation
    risk_report = simulate_risk(schedule, conflicts)

    # 1️⃣2️⃣ Buildability Score
    buildability_score = compute_buildability_score(
        dependency_graph,
        conflicts,
        risk_report
    )

    # 1️⃣3️⃣ Explanation Layer (LLM)
    explanation = generate_explanation({
        "schedule": schedule,
        "conflicts": conflicts,
        "risk": risk_report,
        "buildability_score": buildability_score
    })

    # Final Project State
    project_state.update({
        "structural_twin": structural_twin,
        "quantities": quantities,
        "schedule": schedule,
        "conflicts": conflicts,
        "risk_report": risk_report,
        "buildability_score": buildability_score,
        "explanation": explanation,
        "confidence_overall": min(scale_confidence, structural_twin.get("confidence", 1.0)),
        "status": "Completed"
    })

    # Save JSON Contract
    with open(PROJECT_STATE_FILE, "w") as f:
        json.dump(project_state, f, indent=4)

    return project_state


# =====================================================
# EXECUTION TRIGGER
# =====================================================

if uploaded_file is not None:
    with st.spinner("Running StructuraAI Intelligence Pipeline..."):
        result = run_pipeline(uploaded_file)

    st.success("Pipeline Completed Successfully")

    st.subheader("Buildability Score")
    st.metric("Score", f"{result['buildability_score']} / 100")

    st.subheader("Conflicts Detected")
    st.write(result["conflicts"])

    st.subheader("Risk Report")
    st.write(result["risk_report"])

    st.subheader("AI Engineering Explanation")
    st.write(result["explanation"])

    st.subheader("Exported JSON")
    st.json(result)