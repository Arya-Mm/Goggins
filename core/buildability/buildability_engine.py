import networkx as nx


def calculate_buildability(G, total_duration, conflicts):

    task_count = len(G.nodes)
    conflict_count = len(conflicts)

    # Average slack
    total_slack = sum(G.nodes[n]["slack"] for n in G.nodes)
    avg_slack = total_slack / task_count if task_count > 0 else 0

    # Dependency depth (longest path length)
    try:
        depth = nx.dag_longest_path_length(G)
    except:
        depth = 0

    # Normalize components
    conflict_penalty = conflict_count * 10
    duration_penalty = max(0, total_duration - task_count) * 2
    slack_bonus = avg_slack * 5
    depth_penalty = depth * 2

    score = 100
    score -= conflict_penalty
    score -= duration_penalty
    score -= depth_penalty
    score += slack_bonus

    score = max(0, min(100, int(score)))

    if score > 75:
        level = "High Buildability"
    elif score > 50:
        level = "Moderate Buildability"
    else:
        level = "Low Buildability"

    return {
        "buildability_score": score,
        "buildability_level": level
    }