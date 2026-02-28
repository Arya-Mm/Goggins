# core/ai/buildability_explainer.py

import subprocess
import json


def explain_buildability(buildability_data):
    """
    Uses Ollama to justify buildability score.
    Deterministic context injection.
    """

    context = f"""
You are a senior construction planning engineer.

Project Buildability Data:
Final Score: {buildability_data['final_score']}
Level: {buildability_data['level']}
Conflicts Penalty: {buildability_data['conflict_penalty']}
Dependency Depth Penalty: {buildability_data['dependency_depth_penalty']}
Duration Penalty: {buildability_data['duration_penalty']}
Serial Chain Penalty: {buildability_data['serial_chain_penalty']}
Workforce Penalty: {buildability_data['workforce_penalty']}
Risk Penalty: {buildability_data['risk_penalty']}
Slack Bonus: {buildability_data['slack_bonus']}

Explain clearly why this project received this buildability rating.
Base reasoning strictly on provided data.
"""

    process = subprocess.Popen(
        ["ollama", "run", "mistral"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output, _ = process.communicate(context)
    return output.strip()