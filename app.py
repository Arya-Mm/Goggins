import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import tempfile
import re

from core.pipeline.analyzer import analyze_project
from core.pipeline.streamlit_adapter import adapt_to_dashboard_schema


# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(layout="wide")
st.title("StructuraAI — Autonomous Construction Intelligence")


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def humanize_label(label):
    label = label.replace("_", " ")
    label = re.sub(r"\d+", "", label)
    return label.title()


# ─────────────────────────────────────────
# STRATEGY SELECTION
# ─────────────────────────────────────────
st.subheader("Execution Strategy")

strategy = st.radio(
    "Planning Approach",
    ["Cost Optimized", "Balanced", "Fast Track"],
    horizontal=True
)

if strategy == "Cost Optimized":
    duration_factor = 1.15
    cost_factor = 0.95
elif strategy == "Fast Track":
    duration_factor = 0.85
    cost_factor = 1.12
else:
    duration_factor = 1.0
    cost_factor = 1.0


uploaded_file = st.file_uploader(
    "Upload Structural Blueprint (PDF or DXF)",
    type=["pdf", "dxf"]
)


# ─────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────
if uploaded_file:

    with st.spinner("Analyzing blueprint and generating execution model..."):

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        raw_result = analyze_project(tmp_path)

        if "error" in raw_result:
            st.error(raw_result["error"])
            st.stop()

        data = adapt_to_dashboard_schema(raw_result)

    # =============================
    # BASE METRICS
    # =============================
    base_duration = data["adjusted_metrics"]["duration"]
    base_cost = data["cost_estimation"]["total_project_cost"]
    base_risk = data["adjusted_metrics"]["risk"]
    base_build = data["adjusted_metrics"]["buildability"]

    duration = int(base_duration * duration_factor)
    cost = base_cost * cost_factor

    # =============================
    # EXECUTIVE SNAPSHOT
    # =============================
    st.subheader("Executive Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Detection Confidence",
              f"{round(data['detection_confidence'] * 100, 2)}%")
    c2.metric("Planned Duration (Days)", duration)
    c3.metric("Estimated Budget", f"₹{cost:,.0f}")
    c4.metric("Buildability Score", round(base_build, 2))

    st.divider()

    # =============================
    # MATERIAL QUANTITIES
    # =============================
    st.subheader("Material Quantity Take-Off")

    qty_data = data.get("quantity_takeoff", [])

    if qty_data:
        df_qty = pd.DataFrame(qty_data)
        st.dataframe(df_qty, use_container_width=True)
    else:
        st.info("No material quantities available.")

    st.divider()

    # =============================
    # EXECUTION SEQUENCE (CLEAN BADGES)
    # =============================
    st.subheader("Execution Sequence")

    sequence = data.get("execution_sequence", [])

    if sequence:
        formatted_steps = []

        for step in sequence:
            formatted_steps.append(
                f"""
                <div style="
                    display:inline-block;
                    padding:6px 14px;
                    margin:4px;
                    border-radius:20px;
                    background-color:#1E2A38;
                    color:#E3F2FD;
                    font-size:14px;
                    border:1px solid #2C3E50;">
                    {humanize_label(step)}
                </div>
                """
            )

        st.markdown(
            f"<div style='padding:10px 0;'>{''.join(formatted_steps)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Execution sequence unavailable.")

    st.divider()

    # =============================
    # WHAT-IF SIMULATION
    # =============================
    st.subheader("What-If Scenario Simulation")

    labor_delta = st.slider("Workforce Change (%)", -50, 50, 0)
    delay_delta = st.slider("Material Delay (Days)", -30, 60, 0)
    budget_delta = st.slider("Budget Adjustment (%)", -30, 50, 0)

    labor_eff = 1 - (labor_delta / 100)
    revised_duration = int(duration * labor_eff + delay_delta)

    revised_cost = cost + \
        (base_cost * (labor_delta / 200)) + \
        (base_cost * (delay_delta / 365) * 0.6) + \
        (cost * (budget_delta / 100))

    revised_risk = max(0, min(100,
                              base_risk +
                              delay_delta * 0.5 -
                              labor_delta * 0.3))

    s1, s2, s3 = st.columns(3)
    s1.metric("Revised Duration", revised_duration)
    s2.metric("Revised Budget", f"₹{revised_cost:,.0f}")
    s3.metric("Revised Risk Index", round(revised_risk, 2))

    st.divider()

    # =============================
    # RESOURCE CONFLICTS
    # =============================
    st.subheader("Resource Conflict Detection")

    conflicts = data.get("conflicts", [])

    if conflicts:
        for conflict in conflicts:
            st.markdown(
                f"""
                <div style="
                    padding:14px;
                    margin-bottom:10px;
                    border-radius:10px;
                    background-color:#2B1D1D;
                    border:1px solid #5A2A2A;">
                    <b style="color:#FF6B6B;">Crew Overload</b><br>
                    Time: {conflict.get("time","N/A")} <br>
                    Load: {conflict.get("total_load","N/A")} / Capacity: {conflict.get("capacity","N/A")}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <div style="
                padding:14px;
                border-radius:10px;
                background-color:#1D2B1D;
                border:1px solid #2E7D32;
                color:#A5D6A7;">
                No resource overload conflicts detected.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # =============================
    # DEPENDENCY GRAPH
    # =============================
    st.subheader("Execution Dependency Network")

    graph_data = data.get("dependency_graph", {})
    critical_path = data.get("critical_path", [])

    if graph_data:

        G = nx.DiGraph()
        G.add_nodes_from(graph_data["nodes"])
        G.add_edges_from(graph_data["edges"])

        pos = nx.spring_layout(G, seed=42)

        edge_x, edge_y = [], []

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        node_x, node_y, node_text, node_color = [], [], [], []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(humanize_label(node))
            node_color.append("#E53935" if node in critical_path else "#1E88E5")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode="lines",
            line=dict(width=1, color="#888"),
            hoverinfo="none"
        ))

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="top center",
            marker=dict(size=25, color=node_color),
            hoverinfo="text"
        ))

        fig.update_layout(
            height=500,
            plot_bgcolor="#0F172A",
            paper_bgcolor="#0F172A",
            font=dict(color="white"),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False, visible=False)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =============================
    # TIMELINE
    # =============================
    st.subheader("Project Timeline")

    schedule = data.get("schedule", [])

    if schedule:
        df_schedule = pd.DataFrame(schedule)
        df_schedule["start"] = pd.to_datetime(df_schedule["start"])
        df_schedule["finish"] = pd.to_datetime(df_schedule["finish"])

        fig_timeline = px.timeline(
            df_schedule,
            x_start="start",
            x_end="finish",
            y="task"
        )

        fig_timeline.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_timeline, use_container_width=True)

    st.divider()

    # =============================
    # EXECUTION AUDIT PANEL
    # =============================
    trace = data.get("computation_trace", {})

    st.subheader("Execution Audit Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", trace.get("graph_stats", {}).get("total_nodes", 0))
    col2.metric("Critical Path Length", len(trace.get("critical_path", [])))
    col3.metric("Project Duration (Days)", trace.get("total_duration_days", 0))
    col4.metric("Conflict Count", trace.get("conflict_count", 0))

    st.write("### Risk Drivers")

    risk_breakdown = trace.get("risk_breakdown", {}).get("breakdown", {})
    for k, v in risk_breakdown.items():
        st.write(f"- **{k.replace('_',' ').title()}**: {v}")

    with st.expander("Advanced Technical Trace"):
        st.json(trace)

    st.divider()

    # =============================
    # PDF EXPORT
    # =============================
    if "pdf_path" in raw_result:
        with open(raw_result["pdf_path"], "rb") as f:
            st.download_button(
                label="Download Detailed Project Report",
                data=f,
                file_name="structuraai_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("Upload a structural blueprint to begin analysis.")