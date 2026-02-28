import networkx as nx


def calculate_buildability(G, total_duration, conflicts, risk_data=None):
    """
    Fully transparent deterministic Buildability Engine.
    Backward compatible.
    """

    # ==============================
    # SAFE EXTRACTION
    # ==============================

    task_count = len(G.nodes) if G else 0
    conflict_count = len(conflicts) if conflicts else 0

    # Slack computation (safe)
    total_slack = 0
    slack_nodes = 0

    for n in G.nodes:
        slack = G.nodes[n].get("slack", 0)
        total_slack += slack
        slack_nodes += 1

    avg_slack = total_slack / slack_nodes if slack_nodes > 0 else 0

    # Dependency depth (longest chain)
    try:
        depth = nx.dag_longest_path_length(G)
        critical_path = nx.dag_longest_path(G)
    except:
        depth = 0
        critical_path = []

    # Serial chain estimation (nodes with only 1 outgoing edge)
    serial_chains = sum(1 for n in G.nodes if G.out_degree(n) == 1)

    # Workforce overload detection (if stored)
    workforce_overload_events = 0
    for n in G.nodes:
        if G.nodes[n].get("overloaded", False):
            workforce_overload_events += 1

    # Risk density (normalized)
    risk_score = 0
    if risk_data and "risk_score" in risk_data:
        risk_score = risk_data["risk_score"]

    # ==============================
    # SCORING MODEL
    # ==============================

    base_score = 100

    conflict_penalty = conflict_count * 8
    depth_penalty = depth * 2
    duration_penalty = max(0, total_duration - task_count) * 2
    serial_penalty = serial_chains * 1.5
    workforce_penalty = workforce_overload_events * 5
    risk_penalty = risk_score * 20
    slack_bonus = min(12, avg_slack * 4)

    final_score = (
        base_score
        - conflict_penalty
        - depth_penalty
        - duration_penalty
        - serial_penalty
        - workforce_penalty
        - risk_penalty
        + slack_bonus
    )

    final_score = max(0, min(100, round(final_score, 2)))

    # ==============================
    # RISK LEVEL CLASSIFICATION
    # ==============================

    if final_score >= 85:
        level = "LOW RISK"
    elif final_score >= 70:
        level = "MODERATE"
    elif final_score >= 50:
        level = "HIGH RISK"
    else:
        level = "CRITICAL"

    # ==============================
    # BREAKDOWN STRUCTURE
    # ==============================

    breakdown = {
        "base_score": base_score,
        "conflict_penalty": round(conflict_penalty, 2),
        "dependency_depth_penalty": round(depth_penalty, 2),
        "duration_penalty": round(duration_penalty, 2),
        "serial_chain_penalty": round(serial_penalty, 2),
        "workforce_penalty": round(workforce_penalty, 2),
        "risk_penalty": round(risk_penalty, 2),
        "slack_bonus": round(slack_bonus, 2),
        "final_score": final_score,
        "level": level,
        "critical_path": critical_path,
        "task_count": task_count
    }

    return breakdown