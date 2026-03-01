import streamlit as st
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
if "twin" not in st.session_state:
    st.session_state.twin = None

if "planning_state" not in st.session_state:
    st.session_state.planning_state = None

if "profiling" not in st.session_state:
    st.session_state.profiling = {}

# ─────────────────────────────────────────────
# FILE UPLOAD
# ─────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Upload Blueprint PDFs",
    type=["pdf"],
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
# RUN VISION
# ─────────────────────────────────────────────
if st.button("Run Vision Stage"):

    if not uploaded_files:
        st.warning("Upload at least one PDF.")
        st.stop()

    progress = st.progress(0)

    for file in uploaded_files:

        progress.progress(10)

        result = run_vision_stage(file.read())

        st.session_state.twin = result
        st.session_state.profiling["vision_time"] = result["stage_time"]

        progress.progress(100)

# ─────────────────────────────────────────────
# RUN PLANNING
# ─────────────────────────────────────────────
if st.button("Run Planning Stage"):

    if st.session_state.twin is None:
        st.warning("Run Vision Stage first.")
        st.stop()

    progress = st.progress(0)

    result = run_planning_stage(
        st.session_state.twin["twin"],
        strategy,
        crew,
        productivity,
        curing
    )

    if "error" in result:
        st.error(result["error"])
        st.stop()

    st.session_state.planning_state = result
    st.session_state.profiling["planning_time"] = result["stage_time"]

    progress.progress(100)

# ─────────────────────────────────────────────
# DASHBOARD DISPLAY
# ─────────────────────────────────────────────
state = st.session_state.planning_state

if state:

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
    pos = nx.spring_layout(G, seed=42)

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
        filename = export_pdf(state)
        with open(filename, "rb") as f:
            st.download_button(
                "Download Report",
                f,
                file_name="StructuraAI_Report.pdf"
            )

    # ─────────────────────────────────────────
    # PERFORMANCE PROFILING
    # ─────────────────────────────────────────
    st.subheader("Performance Profiling")

    st.write("Vision Time:",
             round(st.session_state.profiling.get("vision_time", 0),2),
             "sec")

    st.write("Planning Time:",
             round(st.session_state.profiling.get("planning_time", 0),2),
             "sec")