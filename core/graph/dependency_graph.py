import networkx as nx
import math


def generate_tasks_from_twin(
    twin,
    productivity_factor=1.0,
    curing_days=2
):
    tasks = []
    dependencies = []

    # =========================
    # WALLS → BUILD → CURE → INSTALL
    # =========================
    for i, wall in enumerate(twin.get("walls", [])):

        build_id = f"wall_build_{i}"
        cure_id = f"wall_cure_{i}"

        # -----------------------------------
        # WALL BUILD DURATION (Productivity-aware)
        # -----------------------------------
        base_duration = max(
            1,
            math.ceil(wall.get("net_volume_cuft", 1) / 10)
        )

        adjusted_build_duration = max(
            1,
            math.ceil(base_duration / productivity_factor)
        )

        # -----------------------------------
        # BUILD TASK
        # -----------------------------------
        tasks.append({
            "task_id": build_id,
            "duration": adjusted_build_duration,
            "resource": 1,
            "type": "wall_build"
        })

        # -----------------------------------
        # CURING TASK (Scenario adjustable)
        # -----------------------------------
        tasks.append({
            "task_id": cure_id,
            "duration": curing_days,
            "resource": 0,
            "type": "wall_cure"
        })

        dependencies.append((build_id, cure_id))

        # -----------------------------------
        # DOOR INSTALLS
        # -----------------------------------
        for d in range(wall.get("attached_doors", 0)):
            door_id = f"door_install_{i}_{d}"

            tasks.append({
                "task_id": door_id,
                "duration": 1,
                "resource": 1,
                "type": "door_install"
            })

            dependencies.append((cure_id, door_id))

        # -----------------------------------
        # WINDOW INSTALLS
        # -----------------------------------
        for w in range(wall.get("attached_windows", 0)):
            win_id = f"window_install_{i}_{w}"

            tasks.append({
                "task_id": win_id,
                "duration": 1,
                "resource": 1,
                "type": "window_install"
            })

            dependencies.append((cure_id, win_id))

    return tasks, dependencies


def build_dependency_graph(tasks, dependencies):
    G = nx.DiGraph()

    for task in tasks:
        G.add_node(task["task_id"], **task)

    for dep in dependencies:
        G.add_edge(dep[0], dep[1])

    cycle_valid = nx.is_directed_acyclic_graph(G)

    return G, cycle_valid