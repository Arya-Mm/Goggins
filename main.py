from core.vision.vision_engine import VisionEngine
from core.twin.twin_builder import StructuralTwinBuilder
from core.graph.dependency_graph import generate_tasks_from_twin, build_dependency_graph
from core.scheduling.strategy_engine import apply_strategy
from core.scheduling.cpm_engine import run_cpm
from core.scheduling.resource_engine import apply_resource_constraint

from pathlib import Path


def run_demo():
    print("Running StructuraAI Vision + Twin Demo...")

    demo_pdf = Path("core/vision/house_plan.pdf")

    # ===== VISION =====
    vision = VisionEngine()
    vision_output = vision.run(str(demo_pdf))

    # ===== TWIN =====
    twin_builder = StructuralTwinBuilder()
    twin = twin_builder.build(vision_output)

    print("\nDigital Structural Twin:")
    print(twin)

    # ===== DEPENDENCY + SCHEDULING =====
    print("\n--- Dependency & Scheduling Layer ---")

    tasks, dependencies = generate_tasks_from_twin(twin)

    # Choose strategy: fast | balanced | cost
    tasks = apply_strategy(tasks, strategy="balanced")

    G, cycle_valid = build_dependency_graph(tasks, dependencies)

    print("Dependency Graph Valid:", cycle_valid)

    if not cycle_valid:
        print("Cycle detected. Scheduling aborted.")
        return

    G, critical_path, total_duration = run_cpm(G)

    G = apply_resource_constraint(G, capacity=3)

    print("\nTotal Project Duration:", total_duration)
    print("Critical Path:", critical_path)

    print("\nTask Schedule:")
    for node in G.nodes:
        print({
            "task": node,
            "ES": G.nodes[node]["ES"],
            "EF": G.nodes[node]["EF"],
            "Slack": G.nodes[node]["slack"]
        })


if __name__ == "__main__":
    run_demo()