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

        build_id = f"wall_build_{i}"
        cure_id = f"wall_cure_{i}"

        # -----------------------------
        # WALL BUILD DURATION
        # -----------------------------
        volume = wall.get("net_volume_cuft", 10)

        base_duration = max(
            1,
            math.ceil(volume / 8)
        )

        adjusted_build_duration = max(
            1,
            math.ceil(base_duration / productivity_factor)
        )

        tasks.append({
            "task_id": build_id,
            "duration": adjusted_build_duration,
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
        # DOOR + WINDOW INSTALLS
        # -----------------------------
        install_ids = []

        for d in range(wall.get("attached_doors", 0)):
            door_id = f"door_install_{i}_{d}"
            tasks.append({
                "task_id": door_id,
                "duration": 2,
                "resource": 1,
                "type": "door_install"
            })
            install_ids.append(door_id)

        for w in range(wall.get("attached_windows", 0)):
            win_id = f"window_install_{i}_{w}"
            tasks.append({
                "task_id": win_id,
                "duration": 2,
                "resource": 1,
                "type": "window_install"
            })
            install_ids.append(win_id)

        # -----------------------------
        # PARALLEL BATCHING LOGIC
        # -----------------------------
        if install_ids:

            batches = [
                install_ids[x:x + crew_capacity]
                for x in range(0, len(install_ids), crew_capacity)
            ]

            previous_anchor = cure_id

            for batch_index, batch in enumerate(batches):

                batch_anchor = f"batch_{i}_{batch_index}"

                tasks.append({
                    "task_id": batch_anchor,
                    "duration": 0,
                    "resource": 0,
                    "type": "batch_anchor"
                })

                # All installs in batch start after previous anchor
                for task_id in batch:
                    dependencies.append((previous_anchor, task_id))
                    dependencies.append((task_id, batch_anchor))

                previous_anchor = batch_anchor

    return tasks, dependencies


def build_dependency_graph(tasks, dependencies):

    G = nx.DiGraph()

    for task in tasks:
        G.add_node(task["task_id"], **task)

    for dep in dependencies:
        G.add_edge(dep[0], dep[1])

    cycle_valid = nx.is_directed_acyclic_graph(G)

    return G, cycle_valid