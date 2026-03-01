# core/pipeline/streamlit_adapter.py

from datetime import datetime, timedelta
import networkx as nx


def adapt_to_dashboard_schema(result):

    twin = result["twin"]
    quantities = result["quantities"]
    risk = result["risk"]
    buildability = result["buildability"]
    schedule_data = result["schedule"]
    G = schedule_data["graph"]
    total_duration = schedule_data["total_duration"]
    critical_path = schedule_data["critical_path"]

    today = datetime.today()

    # ─────────────────────────────────────
    # SCHEDULE TIMELINE
    # ─────────────────────────────────────
    schedule = []

    for node in G.nodes:
        ES = G.nodes[node].get("ES", 0)
        EF = G.nodes[node].get("EF", 0)
        slack = G.nodes[node].get("slack", 0)

        schedule.append({
            "task": node,
            "start": (today + timedelta(days=ES)).strftime("%Y-%m-%d"),
            "finish": (today + timedelta(days=EF)).strftime("%Y-%m-%d"),
            "duration": EF - ES,
            "slack": slack,
            "phase": node.split("_")[0].capitalize()
        })

    # ─────────────────────────────────────
    # DEPENDENCY GRAPH
    # ─────────────────────────────────────
    nodes = list(G.nodes)
    edges = list(G.edges)

    # ─────────────────────────────────────
    # QUANTITY TAKEOFF
    # ─────────────────────────────────────
    quantity_takeoff = []

    for k, v in quantities["material_quantities"].items():
        quantity_takeoff.append({
            "item": k,
            "quantity": v
        })

    total_cost = quantities["cost_breakdown"]["total_project_cost"]

    # ─────────────────────────────────────
    # NODE-LEVEL RISK MATRIX
    # ─────────────────────────────────────
    risk_matrix = []

    for node in G.nodes:
        depth = 0
        try:
            depth = nx.shortest_path_length(G, source=list(G.nodes)[0], target=node)
        except:
            pass

        slack = G.nodes[node].get("slack", 0)

        node_risk = (
            (5 if node in critical_path else 2) +
            depth * 0.4 +
            (3 if slack == 0 else 1)
        )

        risk_matrix.append({
            "phase": node,
            "risk": round(min(10, node_risk), 2)
        })

    # ─────────────────────────────────────
    # CONFLICTS (REAL PASSTHROUGH)
    # ─────────────────────────────────────
    conflict_details = risk.get("conflict_details", [])

    formatted_conflicts = []

    for c in conflict_details:
        formatted_conflicts.append({
            "type": c.get("type", "Conflict"),
            "description": c.get("description", ""),
            "severity": c.get("severity", "Medium")
        })

    # ─────────────────────────────────────
    # PHASE BREAKDOWN
    # ─────────────────────────────────────
    phase_breakdown_dict = {}

    for task in schedule:
        phase = task["phase"]
        phase_breakdown_dict.setdefault(phase, 0)
        phase_breakdown_dict[phase] += task["duration"]

    phase_breakdown = [
        {"phase": k, "duration": v}
        for k, v in phase_breakdown_dict.items()
    ]

    # ─────────────────────────────────────
    # EXECUTION SEQUENCE
    # ─────────────────────────────────────
    execution_sequence = list(nx.topological_sort(G))

    # ─────────────────────────────────────
    # COMPUTATION TRACE (FULL AUDIT MODE)
    # ─────────────────────────────────────
    computation_trace = {
        "scale_calibration": result.get("scale", {}),
        "total_duration_days": total_duration,
        "critical_path": critical_path,
        "node_slack_values": {
            node: G.nodes[node].get("slack", 0)
            for node in G.nodes
        },
        "conflict_count": len(formatted_conflicts),
        "conflict_details": formatted_conflicts,
        "risk_breakdown": risk,
        "buildability_breakdown": buildability,
        "quantity_breakdown": quantities,
        "graph_stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "graph_density": nx.density(G)
        }
    }

    # ─────────────────────────────────────
    # FINAL STRUCTURED OUTPUT
    # ─────────────────────────────────────
    return {
        "detection_confidence": twin.get("confidence_score", 0) / 100,
        "digital_twin": twin,
        "critical_path": critical_path,
        "execution_sequence": execution_sequence,
        "adjusted_metrics": {
            "duration": total_duration,
            "cost": total_cost,
            "risk": risk.get("risk_score", 0),
            "buildability": buildability.get("final_score", 0)
        },
        "cost_estimation": {
            "currency": "₹",
            "total_project_cost": total_cost
        },
        "quantity_takeoff": quantity_takeoff,
        "schedule": schedule,
        "dependency_graph": {
            "nodes": nodes,
            "edges": edges
        },
        "risk_matrix": risk_matrix,
        "conflicts": formatted_conflicts,
        "phase_breakdown": phase_breakdown,
        "computation_trace": computation_trace
    }