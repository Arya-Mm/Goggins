import os
import json
import logging
from ingestion.loader import DrawingLoader
from vision.detector import StructuralDetector
from twin.builder import DigitalTwinBuilder
from graph.dependency import DependencyEngine
from scheduling.planner import ConstructionPlanner

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("StructuraAI-Core")

class StructuraAICore:
    def __init__(self):
        self.project_state = {
            "project_metadata": {},
            "detected_entities": [],
            "spatial_twin": {},
            "schedule": {},
            "conflicts": [],
            "risk_profile": {},
            "buildability_score": 100
        }

    def execute_pipeline(self, file_path):
        logger.info(f"🚀 Starting Pipeline for: {file_path}")

        # 1. Ingestion
        loader = DrawingLoader(file_path)
        raw_data = loader.load()

        # 2. Vision & Perception (YOLO + Hough + OCR)
        # For now, initializing the detector
        detector = StructuralDetector()
        detections = detector.analyze(raw_data)
        self.project_state["detected_entities"] = detections

        # 3. Digital Twin & Takeoff
        builder = DigitalTwinBuilder()
        self.project_state["spatial_twin"] = builder.generate_twin(detections)

        # 4. Dependency & Scheduling
        dep_engine = DependencyEngine()
        graph = dep_engine.build_graph(self.project_state["spatial_twin"])
        
        planner = ConstructionPlanner()
        self.project_state["schedule"] = planner.generate_strategies(graph)

        # 5. Export Data Contract for Dashboard
        self.export_state()
        logger.info("✅ Pipeline Execution Complete.")

    def export_state(self):
        with open("project_state.json", "w") as f:
            json.dump(self.project_state, f, indent=4)
        logger.info("📂 project_state.json exported for Dashboard.")

if __name__ == "__main__":
    core = StructuraAICore()
    # Replace with actual path during hackathon
    core.execute_pipeline("data/sample_blueprint.png")