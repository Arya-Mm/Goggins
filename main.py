from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from core.ingestion.loader import BlueprintLoader
from core.vision.detector import StructuralDetector

def run_demo():
    print("Running StructuraAI Demo...")

    demo_path = BASE_DIR / "core" / "data" / "demo_blueprint.png"

    loader = BlueprintLoader()
    raw_img, processed_img = loader.load_and_preprocess(str(demo_path))

    detector = StructuralDetector()
    detections = detector.detect(processed_img)

    print("Detections:", detections)

if __name__ == "__main__":
    run_demo()