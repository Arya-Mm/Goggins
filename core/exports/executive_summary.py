# core/exports/executive_summary.py

def generate_executive_summary(
    baseline_duration,
    scenario_duration,
    baseline_risk,
    scenario_risk,
    baseline_buildability,
    scenario_buildability
):
    summary = f"""
================ EXECUTIVE SUMMARY ================

Baseline Duration: {baseline_duration}
Scenario Duration: {scenario_duration}

Baseline Risk Level: {baseline_risk}
Scenario Risk Level: {scenario_risk}

Baseline Buildability: {baseline_buildability}
Scenario Buildability: {scenario_buildability}

--------------------------------------------------

Strategic Insight:
"""

    if scenario_duration < baseline_duration:
        summary += "\n• Scenario reduces project duration."
    else:
        summary += "\n• Scenario does not improve project duration."

    if scenario_buildability != baseline_buildability:
        summary += "\n• Buildability classification changes under scenario."

    summary += "\n• Decision should balance risk exposure vs schedule acceleration."

    return summary