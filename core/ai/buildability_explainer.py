# core/ai/buildability_explainer.py

import subprocess


def explain_buildability(buildability_data):
    """
    Structured, non-hallucinating Buildability Explanation.
    Windows-safe encoding.
    Deterministic context injection.
    """

    context = f"""
You are a deterministic construction analysis engine.

STRICT RULES:
- Use ONLY the numeric data provided.
- Do NOT assume ground conditions.
- Do NOT invent external factors.
- Do NOT speculate.
- Do NOT reference general construction practices.
- Explain strictly how the penalties numerically reduce the score.

Project Data:
Final Score: {buildability_data.get('final_score')}
Level: {buildability_data.get('level')}

Penalties:
Conflict Penalty: {buildability_data.get('conflict_penalty')}
Dependency Depth Penalty: {buildability_data.get('dependency_depth_penalty')}
Duration Penalty: {buildability_data.get('duration_penalty')}
Serial Chain Penalty: {buildability_data.get('serial_chain_penalty')}
Workforce Penalty: {buildability_data.get('workforce_penalty')}
Risk Penalty: {buildability_data.get('risk_penalty')}
Slack Bonus: {buildability_data.get('slack_bonus')}

Explain clearly how these numbers produce the final score.
Keep explanation concise and technical.
"""

    try:
        process = subprocess.Popen(
            ["ollama", "run", "mistral"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",      # ✅ Fix Windows encoding crash
            errors="ignore"        # ✅ Prevent UnicodeDecodeError
        )

        output, error = process.communicate(context, timeout=25)

        if process.returncode != 0:
            return "AI explanation unavailable (Ollama returned error)."

        return output.strip()

    except Exception as e:
        return f"AI explanation unavailable: {str(e)}"