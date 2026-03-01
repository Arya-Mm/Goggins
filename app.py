import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import tempfile

from core.pipeline.analyzer import analyze_project
from core.pipeline.streamlit_adapter import adapt_to_dashboard_schema

# ─────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────
st.set_page_config(layout="wide")
st.title("StructuraAI — Construction Intelligence Platform")

# ─────────────────────────────────────────
# Project Type Selection
# ─────────────────────────────────────────
project_type = st.radio(
    "Project Category",
    ["Residential", "Commercial", "Industrial"],
    horizontal=True
)

st.caption(f"Current Selection: {project_type}")

uploaded_file = st.file_uploader(
    "Upload Structural Blueprint (PDF)",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Running structural analysis..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        raw_result = analyze_project(tmp_path, project_type=project_type)

        if "error" in raw_result:
            st.error(raw_result["error"])
            st.stop()

        data = adapt_to_dashboard_schema(raw_result)

    # ─────────────────────────────────────────
    # KPI Row
    # ─────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Detection Confidence",
                f"{round(data['detection_confidence'] * 100, 2)}%")

    col2.metric("Estimated Duration (days)",
                data["adjusted_metrics"]["duration"])

    col3.metric("Buildability Score",
                data["adjusted_metrics"]["buildability"])

    col4.metric("Overall Risk Index",
                round(data["adjusted_metrics"]["risk"], 2))

    st.divider()

    # ─────────────────────────────────────────
    # Scenario Simulation
    # ─────────────────────────────────────────
    st.subheader("Scenario Planning")

    labor = st.slider("Workforce Available", 5, 100, 20)
    delay = st.slider("Material Delay (days)", 0, 60, 5)
    budget_factor = st.slider("Budget Flexibility", 0.8, 1.5, 1.0)

    base_duration = data["adjusted_metrics"]["duration"]
    base_cost = data["cost_estimation"]["total_project_cost"]
    base_risk = data["adjusted_metrics"]["risk"]

    revised_duration = int(base_duration * (1 + delay / 100))
    revised_cost = base_cost * budget_factor
    revised_risk = min(100, base_risk + delay * 0.3)

    c1, c2, c3 = st.columns(3)
    c1.metric("Revised Duration", revised_duration)
    c2.metric("Revised Budget", f"₹{revised_cost:,.0f}")
    c3.metric("Revised Risk", round(revised_risk, 2))

    st.divider()

    # ─────────────────────────────────────────
    # Interactive Dependency Graph
    # ─────────────────────────────────────────
    st.subheader("Execution Flow & Dependencies")

    graph_data = data.get("dependency_graph", {})
    critical_path = data.get("critical_path", [])

    show_only_critical = st.checkbox("Highlight Critical Path Only")

    if graph_data:

        G = nx.DiGraph()
        G.add_nodes_from(graph_data["nodes"])
        G.add_edges_from(graph_data["edges"])

        pos = nx.spring_layout(G, k=0.8, iterations=100, seed=42)

        edge_x, edge_y = [], []
        crit_x, crit_y = [], []

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]

            if edge[0] in critical_path and edge[1] in critical_path:
                crit_x += [x0, x1, None]
                crit_y += [y0, y1, None]
            elif not show_only_critical:
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1.5, color="#B0B0B0"),
            hoverinfo="none",
            mode="lines"
        )

        critical_trace = go.Scatter(
            x=crit_x,
            y=crit_y,
            line=dict(width=4, color="#C62828"),
            hoverinfo="none",
            mode="lines"
        )

        node_x, node_y, node_text, node_color = [], [], [], []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

            if node in critical_path:
                node_color.append("#C62828")
            else:
                node_color.append("#2E4053")

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="top center",
            hovertemplate="<b>%{text}</b>",
            marker=dict(
                size=28,
                color=node_color,
                line=dict(width=2, color="#FFFFFF")
            )
        )

        fig_graph = go.Figure(data=[edge_trace, critical_trace, node_trace])

        fig_graph.update_layout(
            height=500,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False)
        )

        st.plotly_chart(fig_graph, use_container_width=True)

        st.markdown(
            """
            🔴 **Critical Path** — Any delay here impacts final delivery  
            ⚫ **Parallel Tasks** — Independent or buffered activities
            """
        )

    st.divider()

    # ─────────────────────────────────────────
    # Risk Overview
    # ─────────────────────────────────────────
    st.subheader("Risk Profile")

    if data["risk_matrix"]:
        df_risk = pd.DataFrame(data["risk_matrix"])

        fig = px.bar(
            df_risk,
            x="phase",
            y="risk",
            color="risk",
            color_continuous_scale="Reds"
        )

        fig.update_layout(
            title="Risk Distribution Across Phases",
            xaxis_title="Project Phase",
            yaxis_title="Risk Index",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ─────────────────────────────────────────
    # Timeline
    # ─────────────────────────────────────────
    st.subheader("Execution Timeline")

    if data["schedule"]:
        df_schedule = pd.DataFrame(data["schedule"])
        df_schedule["start"] = pd.to_datetime(df_schedule["start"])
        df_schedule["finish"] = pd.to_datetime(df_schedule["finish"])

        fig = px.timeline(
            df_schedule,
            x_start="start",
            x_end="finish",
            y="task"
        )

        fig.update_yaxes(autorange="reversed")

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ─────────────────────────────────────────
    # PDF Download
    # ─────────────────────────────────────────
    if "pdf_path" in raw_result:
        with open(raw_result["pdf_path"], "rb") as f:
            st.download_button(
                label="Download Project Intelligence Report",
                data=f,
                file_name="structuraai_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("Upload a structural blueprint to begin.")