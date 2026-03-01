# core/pipeline/streamlit_adapter.py

from datetime import datetime, timedelta


def adapt_to_dashboard_schema(result):

    twin = result["twin"]
    quantities = result["quantities"]
    risk = result["risk"]
    buildability = result["buildability"]
    schedule_data = result["schedule"]
    G = schedule_data["graph"]

    # -----------------------------
    # Build Real Schedule Timeline (FIXED)
    # -----------------------------
    today = datetime.today()

    schedule = []

    for node in G.nodes:

        ES = G.nodes[node].get("ES", 0)
        EF = G.nodes[node].get("EF", 0)

        start = today + timedelta(days=ES)
        finish = today + timedelta(days=EF)

        schedule.append({
            "task": node,
            "start": start.strftime("%Y-%m-%d"),
            "finish": finish.strftime("%Y-%m-%d")
        })

    # -----------------------------
    # Build Dependency Graph
    # -----------------------------
    nodes = list(G.nodes)
    edges = list(G.edges)

    # -----------------------------
    # Quantity Takeoff
    # -----------------------------
    quantity_takeoff = []

    for k, v in quantities["material_quantities"].items():
        quantity_takeoff.append({
            "category": "Material",
            "type": "Material",
            "item": k,
            "quantity": v,
            "unit": "Unit"
        })

    # -----------------------------
    # Cost Breakdown
    # -----------------------------
    total_cost = quantities["cost_breakdown"]["total_project_cost"]

    cost_estimation = {
        "currency": "₹",
        "total_project_cost": total_cost,
        "phase_costs": [],
        "resource_cost_breakdown": []
    }

    # -----------------------------
    # Risk Matrix
    # -----------------------------
    risk_matrix = []

    for node in nodes:
        risk_matrix.append({
            "phase": node,
            "risk": min(5, int(risk["risk_score"] / 20))
        })

    # -----------------------------
    # Conflicts
    # -----------------------------
    conflicts = []

    if risk["breakdown"]["conflict_risk"] > 0:
        conflicts.append({
            "type": "Scheduling Conflict",
            "description": "Resource overload detected",
            "severity": "High"
        })

    # -----------------------------
    # Final JSON for Streamlit
    # -----------------------------
    return {
        "detection_confidence": twin.get("confidence_score", 0) / 100,
        "digital_twin": {
            "columns": twin.get("columns", []),
            "beams": twin.get("beams", []),
            "slabs": twin.get("slabs", [])
        },
        "critical_path": schedule_data["critical_path"],
        "resource_overloads": [],
        "adjusted_metrics": {
            "duration": schedule_data["total_duration"],
            "cost": total_cost,
            "risk": risk["risk_score"] / 20,
            "buildability": buildability["final_score"]
        },
        "cost_estimation": cost_estimation,
        "quantity_takeoff": quantity_takeoff,
        "schedule": schedule,
        "dependency_graph": {
            "nodes": nodes,
            "edges": edges
        },
        "risk_matrix": risk_matrix,
        "conflicts": conflicts,
        "phase_breakdown": [],
        "execution_strategies": {},
        "strategy_selected": "Baseline",
        "what_if_parameters": {},
        "ai_explanation": {
            "summary": "AI-generated construction intelligence report.",
            "risk_reasoning": "Risk derived from CPM depth, serial chain, and uncertainty propagation.",
            "recommendation": "Optimize workforce allocation to improve buildability."
        }
    }