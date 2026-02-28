def calculate_risk(total_duration, conflict_count):

    risk_score = 0

    if total_duration > 10:
        risk_score += 10

    risk_score += conflict_count * 5

    if risk_score < 10:
        level = "Low"
    elif risk_score < 25:
        level = "Moderate"
    else:
        level = "High"

    return {
        "risk_score": risk_score,
        "risk_level": level
    }