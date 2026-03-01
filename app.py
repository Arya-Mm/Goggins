import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import tempfile

from core.pipeline.analyzer import analyze_project
from core.pipeline.streamlit_adapter import adapt_to_dashboard_schema

# ─────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────
st.set_page_config(layout="wide")
st.title("StructuraAI — Construction Intelligence Platform")

# ─────────────────────────────────────────
# Execution Strategy Selector (NEW)
# ─────────────────────────────────────────
st.subheader("Execution Strategy")

strategy = st.radio(
    "Select planning strategy",
    ["Cost Optimized", "Balanced", "Fast Track"],
    horizontal=True
)

st.caption(
    "Cost Optimized reduces crew and extends timeline. "
    "Balanced maintains baseline configuration. "
    "Fast Track increases parallel execution and reduces schedule."
)

# Strategy multipliers
if strategy == "Cost Optimized":
    strategy_duration_factor = 1.15
    strategy_cost_factor = 0.95
elif strategy == "Fast Track":
    strategy_duration_factor = 0.85
    strategy_cost_factor = 1.10
else:  # Balanced
    strategy_duration_factor = 1.0
    strategy_cost_factor = 1.0

uploaded_file = st.file_uploader(
    "Upload Structural Blueprint (PDF)",
    type=["pdf"]
)

# ─────────────────────────────────────────
# Main Processing
# ─────────────────────────────────────────
if uploaded_file:

    with st.spinner("Analyzing structural drawing..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        raw_result = analyze_project(tmp_path)

        if "error" in raw_result:
            st.error(raw_result["error"])
            st.stop()

        data = adapt_to_dashboard_schema(raw_result)

    # ─────────────────────────────────────────
    # Base Metrics
    # ─────────────────────────────────────────
    base_duration = data["adjusted_metrics"]["duration"]
    base_cost = data["cost_estimation"]["total_project_cost"]
    base_risk = data["adjusted_metrics"]["risk"]
    base_build = data["adjusted_metrics"]["buildability"]

    strategy_duration = int(base_duration * strategy_duration_factor)
    strategy_cost = base_cost * strategy_cost_factor

    st.subheader("Project Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Detection Confidence",
              f"{round(data['detection_confidence']*100,2)}%")
    c2.metric("Planned Duration (days)", strategy_duration)
    c3.metric("Estimated Budget", f"₹{strategy_cost:,.0f}")
    c4.metric("Buildability Score", base_build)

    st.divider()

    # ─────────────────────────────────────────
    # Advanced Scenario Simulation (± Values)
    # ─────────────────────────────────────────
    st.subheader("Scenario Adjustment")

    labor_delta = st.slider(
        "Workforce Adjustment (%)",
        -50, 50, 0
    )

    delay_delta = st.slider(
        "Material Delay (days)",
        -30, 60, 0
    )

    budget_delta = st.slider(
        "Budget Adjustment (%)",
        -30, 50, 0
    )

    # Revised logic (supports negative)
    labor_factor = 1 - (labor_delta / 100)
    revised_duration = int(strategy_duration * labor_factor + delay_delta)

    revised_cost = strategy_cost * (1 + budget_delta / 100)
    revised_risk = max(0, min(100, base_risk + delay_delta*0.4 - labor_delta*0.2))

    s1, s2, s3 = st.columns(3)
    s1.metric("Revised Duration", revised_duration)
    s2.metric("Revised Budget", f"₹{revised_cost:,.0f}")
    s3.metric("Revised Risk Index", round(revised_risk,2))

    st.divider()

    # ─────────────────────────────────────────
    # Enterprise Dependency Graph
    # ─────────────────────────────────────────
    st.subheader("Execution Network")

    graph_data = data.get("dependency_graph", {})
    critical_path = data.get("critical_path", [])

    highlight_only = st.checkbox("Show only critical path")

    if graph_data:

        G = nx.DiGraph()
        G.add_nodes_from(graph_data["nodes"])
        G.add_edges_from(graph_data["edges"])

        pos = nx.spring_layout(G, k=0.9, iterations=120, seed=42)

        edge_x, edge_y = [], []
        crit_x, crit_y = [], []

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]

            if edge[0] in critical_path and edge[1] in critical_path:
                crit_x += [x0, x1, None]
                crit_y += [y0, y1, None]
            elif not highlight_only:
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=1.2, color="#B0B0B0"),
            hoverinfo="none"
        )

        critical_trace = go.Scatter(
            x=crit_x,
            y=crit_y,
            mode="lines",
            line=dict(width=4, color="#C62828"),
            hoverinfo="none"
        )

        node_x, node_y, node_text, node_color = [], [], [], []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

            node_color.append(
                "#C62828" if node in critical_path else "#2E4053"
            )

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="top center",
            marker=dict(
                size=30,
                color=node_color,
                line=dict(width=2, color="#FFFFFF")
            ),
            hovertemplate="<b>%{text}</b><extra></extra>"
        )

        fig = go.Figure(data=[edge_trace, critical_trace, node_trace])

        fig.update_layout(
            height=520,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False, visible=False)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Red nodes and connections indicate the critical execution path. "
            "Delays here directly affect final completion."
        )

    st.divider()

    # ─────────────────────────────────────────
    # Risk Distribution
    # ─────────────────────────────────────────
    st.subheader("Risk by Phase")

    if data["risk_matrix"]:
        df_risk = pd.DataFrame(data["risk_matrix"])

        fig_risk = px.bar(
            df_risk,
            x="phase",
            y="risk",
            color="risk",
            color_continuous_scale="Reds"
        )

        fig_risk.update_layout(
            xaxis_title="Project Phase",
            yaxis_title="Risk Index"
        )

        st.plotly_chart(fig_risk, use_container_width=True)

    st.divider()

    # ─────────────────────────────────────────
    # Timeline
    # ─────────────────────────────────────────
    st.subheader("Execution Timeline")

    if data["schedule"]:
        df_schedule = pd.DataFrame(data["schedule"])
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

    # ─────────────────────────────────────────
    # PDF Export
    # ─────────────────────────────────────────
    if "pdf_path" in raw_result:
        with open(raw_result["pdf_path"], "rb") as f:
            st.download_button(
                label="Download Full Intelligence Report",
                data=f,
                file_name="structuraai_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("Upload a structural blueprint to begin.")