import math


def apply_strategy(tasks, strategy="balanced"):
    modified = []

    for task in tasks:
        new_task = task.copy()

        if strategy == "fast":
            new_task["duration"] = max(1, math.ceil(task["duration"] * 0.8))
            new_task["resource"] += 1

        elif strategy == "cost":
            new_task["duration"] = math.ceil(task["duration"] * 1.2)
            new_task["resource"] = max(1, task["resource"] - 1)

        modified.append(new_task)

    return modified