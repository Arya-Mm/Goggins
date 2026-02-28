# core/utils/heat_visualizer.py

def classify_heat(score, inverse=False):
    """
    Returns (emoji, color_tag, label)
    inverse=True means higher score is worse (like risk)
    """

    if inverse:
        if score >= 0.7:
            return "🔴", "RED", "CRITICAL"
        elif score >= 0.4:
            return "🟡", "YELLOW", "MODERATE"
        else:
            return "🟢", "GREEN", "LOW"
    else:
        if score >= 85:
            return "🟢", "GREEN", "LOW RISK"
        elif score >= 70:
            return "🟡", "YELLOW", "MODERATE"
        elif score >= 50:
            return "🟠", "ORANGE", "HIGH"
        else:
            return "🔴", "RED", "CRITICAL"