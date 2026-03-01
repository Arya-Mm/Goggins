# core/graph/dependency_graph.py

import networkx as nx
import math


def generate_tasks_from_twin(
    twin,
    productivity_factor=0.6,
    curing_days=5,
    crew_capacity=3  # kept for compatibility but NOT used for dependencies
):

    tasks = []
    dependencies = []

    for i, wall in enumerate(twin.get("walls", [])):

        # -----------------------------
        # WALL BUILD
        # -----------------------------
        build_id = f"wall_build_{i}"
        cure_id = f"wall_cure_{i}"

        volume = wall.get("net_volume_cuft", 10)

        build_duration = max(
            1,
            math.ceil((volume / 8) / productivity_factor)
        )

        tasks.append({
            "task_id": build_id,
            "duration": build_duration,
            "resource": 1,
            "type": "wall_build"
        })

        tasks.append({
            "task_id": cure_id,
            "duration": curing_days,
            "resource": 0,
            "type": "wall_cure"
        })

        dependencies.append((build_id, cure_id))

        # -----------------------------
        # DOOR INSTALLS (PARALLEL)
        # -----------------------------
        for d in range(wall.get("attached_doors", 0)):
            door_id = f"door_install_{i}_{d}"

            tasks.append({
                "task_id": door_id,
                "duration": 2,
                "resource": 1,
                "type": "door_install"
            })

            # Logical dependency only
            dependencies.append((cure_id, door_id))

        # -----------------------------
        # WINDOW INSTALLS (PARALLEL)
        # -----------------------------
        for w in range(wall.get("attached_windows", 0)):
            win_id = f"window_install_{i}_{w}"

            tasks.append({
                "task_id": win_id,
                "duration": 2,
                "resource": 1,
                "type": "window_install"
            })

            dependencies.append((cure_id, win_id))

        # -----------------------------
        # FINISHING PHASE
        # -----------------------------
        finishing_id = f"finishing_{i}"

        tasks.append({
            "task_id": finishing_id,
            "duration": 6,
            "resource": 2,
            "type": "finishing"
        })

        # Finishing depends on ALL installs for this wall
        for t in tasks:
            if t["task_id"].startswith(f"door_install_{i}_") or \
               t["task_id"].startswith(f"window_install_{i}_"):
                dependencies.append((t["task_id"], finishing_id))

    return tasks, dependencies


def build_dependency_graph(tasks, dependencies):

    G = nx.DiGraph()

    for task in tasks:
        G.add_node(task["task_id"], **task)

    for dep in dependencies:
        G.add_edge(dep[0], dep[1])

    cycle_valid = nx.is_directed_acyclic_graph(G)

    return G, cycle_valid