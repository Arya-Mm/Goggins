from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from pathlib import Path


def run_demo():
    print("Running StructuraAI Vision + Twin Demo...")

    demo_pdf = Path("core/vision/house_plan.pdf")

    vision = VisionEngine()
    vision_output = vision.run(str(demo_pdf))

    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    print("\nDigital Structural Twin:")
    print(twin)


if __name__ == "__main__":
    run_demo()