def calculate_risk(total_duration, conflicts, G=None, twin=None, critical_path=None):

    # -----------------------------------
    # Task Counts (Exclude batch anchors)
    # -----------------------------------
    if G:
        execution_nodes = [
            n for n in G.nodes
            if not str(n).startswith("batch_")
        ]
        total_tasks = len(execution_nodes)
    else:
        total_tasks = 1

    conflict_count = len(conflicts) if isinstance(conflicts, list) else conflicts

    # -----------------------------------
    # 1️⃣ Duration Risk
    # -----------------------------------
    duration_risk = total_duration * 2

    # -----------------------------------
    # 2️⃣ Critical Path Sensitivity
    # -----------------------------------
    if critical_path and total_tasks > 0:

        execution_cp = [
            n for n in critical_path
            if not str(n).startswith("batch_")
        ]

        cp_ratio = len(execution_cp) / total_tasks
        critical_risk = cp_ratio * 25
    else:
        critical_risk = 0

    # -----------------------------------
    # 3️⃣ Serial Chain Risk
    # -----------------------------------
    if critical_path:
        execution_cp = [
            n for n in critical_path
            if not str(n).startswith("batch_")
        ]
        longest_chain = len(execution_cp)
    else:
        longest_chain = 0

    chain_risk = max(0, longest_chain - 4) * 3

    # -----------------------------------
    # 4️⃣ Conflict Risk
    # -----------------------------------
    conflict_risk = conflict_count * 5

    # -----------------------------------
    # 5️⃣ CONFIDENCE & UNCERTAINTY RISK (UPGRADED)
    # -----------------------------------
    uncertainty_risk = 0

    if twin:

        # 🔹 A. Confidence score propagation
        confidence_score = twin.get("confidence_score", 100)
        confidence_risk = max(0, (100 - confidence_score) * 0.4)

        # 🔹 B. Wall-level dimension uncertainty
        dimension_uncertainty = 0
        for wall in twin.get("walls", []):
            if wall.get("dimension_uncertain", False):
                dimension_uncertainty += 10

        # 🔹 C. Summary-level uncertain wall tracking
        summary_uncertain = twin.get("summary", {}).get("uncertain_walls", 0)
        summary_uncertainty_risk = summary_uncertain * 8

        uncertainty_risk = (
            confidence_risk +
            dimension_uncertainty +
            summary_uncertainty_risk
        )

    # -----------------------------------
    # TOTAL RISK SCORE
    # -----------------------------------
    raw_score = (
        duration_risk +
        critical_risk +
        chain_risk +
        conflict_risk +
        uncertainty_risk
    )

    risk_score = max(0, min(100, round(raw_score, 2)))

    # -----------------------------------
    # Risk Level Classification (Improved)
    # -----------------------------------
    if risk_score < 25:
        risk_level = "Low"
    elif risk_score < 60:
        risk_level = "Moderate"
    elif risk_score < 85:
        risk_level = "High"
    else:
        risk_level = "Critical"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "breakdown": {
            "duration_risk": round(duration_risk, 2),
            "critical_path_risk": round(critical_risk, 2),
            "serial_chain_risk": round(chain_risk, 2),
            "conflict_risk": round(conflict_risk, 2),
            "uncertainty_risk": round(uncertainty_risk, 2)
        }
    }