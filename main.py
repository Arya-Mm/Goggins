import json
import os
from datetime import datetime

# --- Module Imports (will implement layer by layer) ---
from core.ingestion.loader import load_blueprint
from core.vision.detector import detect_structural_elements
from core.vision.wall_hough import detect_walls_hough
from core.vision.ocr import extract_dimensions
from core.twin.scale import calibrate_scale
from core.twin.builder import build_structural_twin
from core.twin.takeoff import compute_quantities
from core.graph.dependency import build_dependency_graph
from core.scheduling.planner import generate_schedule
from core.conflict.checker import detect_conflicts
from core.risk.simulator import simulate_risk
from core.optimization.buildability import compute_buildability_score
from core.ai.explainer import generate_explanation


OUTPUT_DIR = "exports"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_json(data, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[✓] Exported: {path}")


def run_pipeline(image_path: str):
    print("\n--- STRUCTURAAI PIPELINE START ---\n")

    project_state = {
        "timestamp": str(datetime.now()),
        "input_image": image_path,
        "confidence_summary": {},
        "scale_factor": None,
        "schedule": {},
        "conflicts": [],
        "risk_analysis": {},
        "buildability_score": None,
        "explanation": ""
    }

    # 1️⃣ Blueprint Input & Loading
    blueprint = load_blueprint(image_path)

    # 2️⃣ YOLO Detection
    detections = detect_structural_elements(blueprint)

    # 3️⃣ Rule-Based Wall Detection
    walls = detect_walls_hough(blueprint)

    # 4️⃣ OCR Dimension Extraction
    dimensions = extract_dimensions(blueprint)

    # 5️⃣ Scale Calibration
    scale_factor = calibrate_scale(dimensions)
    project_state["scale_factor"] = scale_factor

    # 6️⃣ Digital Structural Twin
    structural_twin = build_structural_twin(
        detections=detections,
        walls=walls,
        scale_factor=scale_factor
    )

    export_json(structural_twin, "detected_structure.json")

    # 7️⃣ Quantity Takeoff
    quantities = compute_quantities(structural_twin)
    structural_twin["quantities"] = quantities

    # 8️⃣ Dependency Graph
    dependency_graph = build_dependency_graph(structural_twin)

    # 9️⃣ Scheduling
    schedule = generate_schedule(dependency_graph, strategy="Balanced")
    project_state["schedule"] = schedule

    # 🔟 Conflict Detection
    conflicts = detect_conflicts(schedule)
    project_state["conflicts"] = conflicts

    # 1️⃣1️⃣ Risk Simulation
    risk_report = simulate_risk(schedule, conflicts)
    project_state["risk_analysis"] = risk_report

    # 1️⃣2️⃣ Buildability Score
    score = compute_buildability_score(schedule, conflicts, risk_report)
    project_state["buildability_score"] = score

    # 1️⃣3️⃣ Explanation Layer
    explanation = generate_explanation(project_state)
    project_state["explanation"] = explanation

    # Final Export
    export_json(project_state, "project_state.json")

    print("\n--- PIPELINE COMPLETE ---\n")
    return project_state


if __name__ == "__main__":
    test_image = "data/sample_blueprint.jpg"
    run_pipeline(test_image)