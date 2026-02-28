import networkx as nx


def calculate_buildability(G, total_duration, conflicts):

    task_count = len(G.nodes)
    conflict_count = len(conflicts)

    # Average slack
    total_slack = sum(G.nodes[n]["slack"] for n in G.nodes)
    avg_slack = total_slack / task_count if task_count > 0 else 0

    # Dependency depth
    try:
        depth = nx.dag_longest_path_length(G)
    except:
        depth = 0

    score = 100

    # 🔥 HARD PENALTIES
    score -= conflict_count * 20
    score -= depth * 3
    score -= max(0, total_duration - task_count) * 3

    # Slack bonus (but limited)
    score += min(10, avg_slack * 4)

    score = max(0, min(100, int(score)))

    if score >= 80:
        level = "High Buildability"
    elif score >= 60:
        level = "Moderate Buildability"
    else:
        level = "Low Buildability"

    return {
        "buildability_score": score,
        "buildability_level": level
    }