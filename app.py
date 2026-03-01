import streamlit as st
import threading
import time
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
from main import run_vision_stage, run_planning_stage, export_pdf

st.set_page_config(layout="wide")

st.title("STRUCTURA AI — Production Intelligence")

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "twin_cache" not in st.session_state:
    st.session_state.twin_cache = None

if "dashboard_state" not in st.session_state:
    st.session_state.dashboard_state = None

if "profiling" not in st.session_state:
    st.session_state.profiling = {}

# ─────────────────────────────────────────────
# FILE UPLOAD (MULTI-FILE SUPPORT)
# ─────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Upload Blueprint Files",
    type=["pdf", "png", "jpg"],
    accept_multiple_files=True
)

# ─────────────────────────────────────────────
# SIDEBAR CONTROLS
# ─────────────────────────────────────────────
strategy = st.sidebar.selectbox(
    "Strategy", ["Balanced", "FastTrack", "CostOptimized"]
)

crew = st.sidebar.slider("Crew Capacity", 1, 6, 2)
productivity = st.sidebar.slider("Productivity", 0.5, 1.5, 1.0)
curing = st.sidebar.slider("Curing Days", 1, 5, 2)

# ─────────────────────────────────────────────
# RUN VISION (HEAVY — ONLY ONCE)
# ─────────────────────────────────────────────
if st.button("Run Vision Stage"):

    progress = st.progress(0)
    status = st.empty()

    for file in uploaded_files:

        status.text("Running Vision Engine...")
        progress.progress(10)

        result = run_vision_stage(file)

        st.session_state.twin_cache = result
        st.session_state.profiling["vision_time"] = result["stage_time"]

        progress.progress(100)
        status.text("Vision Stage Complete")

# ─────────────────────────────────────────────
# RUN PLANNING (FAST RE-RUN)
# ─────────────────────────────────────────────
if st.button("Run Planning Stage"):

    if st.session_state.twin_cache is None:
        st.warning("Run Vision stage first.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    status.text("Running Scheduling + Intelligence...")
    progress.progress(30)

    result = run_planning_stage(
        st.session_state.twin_cache["twin"],
        strategy,
        crew,
        productivity,
        curing
    )

    st.session_state.dashboard_state = result
    st.session_state.profiling["planning_time"] = result["stage_time"]

    progress.progress(100)
    status.text("Planning Stage Complete")

# ─────────────────────────────────────────────
# DISPLAY DASHBOARD
# ─────────────────────────────────────────────
state = st.session_state.dashboard_state

if state:

    st.subheader("Duration")
    st.metric("Total Duration", state["duration"])

    st.subheader("Conflicts")
    for c in state["conflicts"]:
        st.warning(c.get("description"))

    st.subheader("Risk")
    df_risk = pd.DataFrame(state["risk"]["phase_risk"])
    fig = px.bar(df_risk, x="phase", y="risk")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Dependency Graph")
    G = state["graph"]
    pos = nx.spring_layout(G)

    edge_x, edge_y = [], []
    for e in G.edges():
        x0,y0 = pos[e[0]]
        x1,y1 = pos[e[1]]
        edge_x.extend([x0,x1,None])
        edge_y.extend([y0,y1,None])

    node_x, node_y = [], []
    for n in G.nodes():
        x,y = pos[n]
        node_x.append(x)
        node_y.append(y)

    fig_graph = go.Figure()
    fig_graph.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines"))
    fig_graph.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers+text", text=list(G.nodes())))
    st.plotly_chart(fig_graph, use_container_width=True)

    # ─────────────────────────────────────────
    # PDF EXPORT
    # ─────────────────────────────────────────
    if st.button("Generate PDF Report"):
        pdf_path = export_pdf(state)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download Report",
                f,
                file_name="StructuraAI_Report.pdf"
            )

    # ─────────────────────────────────────────
    # PERFORMANCE PROFILING
    # ─────────────────────────────────────────
    st.subheader("Performance Profiling")

    vision_time = st.session_state.profiling.get("vision_time", 0)
    planning_time = st.session_state.profiling.get("planning_time", 0)

    st.write("Vision Stage Time:", round(vision_time,2), "sec")
    st.write("Planning Stage Time:", round(planning_time,2), "sec")