# core/graph/dependency_graph.py

import networkx as nx
import math


def generate_tasks_from_twin(
    twin,
    productivity_factor=0.6,
    curing_days=5,
    crew_capacity=3
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
            2,
            math.ceil((volume / 6) / productivity_factor)
        )

        tasks.append({
            "task_id": build_id,
            "duration": build_duration,
            "resource": 2,
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
        # DOOR INSTALLS (VARIABLE DURATIONS)
        # -----------------------------
        door_ids = []

        for d in range(wall.get("attached_doors", 0)):
            door_id = f"door_install_{i}_{d}"

            # variable duration (creates asymmetry)
            duration = 1 + (d % 3)

            tasks.append({
                "task_id": door_id,
                "duration": duration,
                "resource": 1,
                "type": "door_install"
            })

            dependencies.append((cure_id, door_id))
            door_ids.append(door_id)

        # -----------------------------
        # WINDOW INSTALLS (VARIABLE DURATIONS)
        # -----------------------------
        window_ids = []

        for w in range(wall.get("attached_windows", 0)):
            win_id = f"window_install_{i}_{w}"

            duration = 2 + (w % 2)

            tasks.append({
                "task_id": win_id,
                "duration": duration,
                "resource": 1,
                "type": "window_install"
            })

            dependencies.append((cure_id, win_id))
            window_ids.append(win_id)

        # -----------------------------
        # STRUCTURAL COMPLETION NODE
        # -----------------------------
        structural_complete = f"structural_complete_{i}"

        tasks.append({
            "task_id": structural_complete,
            "duration": 0,
            "resource": 0,
            "type": "milestone"
        })

        # Structural completion waits for longest install only
        # (instead of all installs forcing chain)

        if door_ids:
            dependencies.append((max(door_ids), structural_complete))

        if window_ids:
            dependencies.append((max(window_ids), structural_complete))

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

        dependencies.append((structural_complete, finishing_id))

    return tasks, dependencies


def build_dependency_graph(tasks, dependencies):

    G = nx.DiGraph()

    for task in tasks:
        G.add_node(task["task_id"], **task)

    for dep in dependencies:
        G.add_edge(dep[0], dep[1])

    cycle_valid = nx.is_directed_acyclic_graph(G)

    return G, cycle_valid