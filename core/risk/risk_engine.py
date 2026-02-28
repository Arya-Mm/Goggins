def calculate_risk(total_duration, conflict_count):

    duration_factor = total_duration * 2
    conflict_factor = conflict_count * 10

    risk_score = duration_factor + conflict_factor

    if risk_score < 15:
        level = "Low"
    elif risk_score < 40:
        level = "Moderate"
    else:
        level = "High"

    return {
        "risk_score": risk_score,
        "risk_level": level
    }