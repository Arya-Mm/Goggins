from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from core.vision.vision_engine import VisionEngine


def run_demo():
    print("Running StructuraAI Vision Demo...")

    demo_pdf = BASE_DIR / "core" / "vision" / "house_plan.pdf"  # put test pdf here

    engine = VisionEngine()
    result = engine.run(str(demo_pdf))

    print("Vision Output:")
    print(result)


if __name__ == "__main__":
    run_demo()