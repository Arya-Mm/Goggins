def calculate_risk(total_duration, conflicts, G=None, twin=None, critical_path=None):

    total_tasks = len(G.nodes) if G else 1
    conflict_count = len(conflicts) if isinstance(conflicts, list) else conflicts

    # -----------------------------------
    # 1️⃣ Duration Risk
    # -----------------------------------
    duration_risk = total_duration * 2

    # -----------------------------------
    # 2️⃣ Critical Path Sensitivity
    # -----------------------------------
    if critical_path and total_tasks > 0:
        cp_ratio = len(critical_path) / total_tasks
        critical_risk = cp_ratio * 25
    else:
        critical_risk = 0

    # -----------------------------------
    # 3️⃣ Serial Chain Risk
    # -----------------------------------
    longest_chain = 0

    if critical_path:
        longest_chain = len(critical_path)

    chain_risk = max(0, longest_chain - 4) * 3

    # -----------------------------------
    # 4️⃣ Conflict Risk
    # -----------------------------------
    conflict_risk = conflict_count * 5

    # -----------------------------------
    # 5️⃣ Dimension Uncertainty Risk
    # -----------------------------------
    uncertainty_risk = 0

    if twin:
        uncertain_walls = twin.get("summary", {}).get("uncertain_walls", 0)
        uncertainty_risk = uncertain_walls * 8

    # -----------------------------------
    # TOTAL
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
    # Risk Level Classification
    # -----------------------------------
    if risk_score < 25:
        risk_level = "Low"
    elif risk_score < 60:
        risk_level = "Moderate"
    else:
        risk_level = "High"

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