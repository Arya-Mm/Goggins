import streamlit as st
from main import run_engine
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="StructuraAI — Command Center",
    page_icon="🏗️"
)

# ─────────────────────────────────────────────
# ENGINE CACHE (Heavy Vision + CPM)
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cached_engine(strategy, crew, productivity, curing):
    return run_engine(
        strategy=strategy,
        crew_capacity=crew,
        productivity_factor=productivity,
        curing_days=curing
    )

# ─────────────────────────────────────────────
# SIDEBAR CONTROLS
# ─────────────────────────────────────────────
st.sidebar.title("⚙ Execution Controls")

strategy = st.sidebar.selectbox(
    "Strategy",
    ["Balanced", "FastTrack", "CostOptimized"]
)

crew = st.sidebar.slider("Crew Capacity", 1, 6, 2)
productivity = st.sidebar.slider("Productivity", 0.5, 1.5, 1.0)
curing = st.sidebar.slider("Curing Days", 1, 5, 2)

run_btn = st.sidebar.button("Run StructuraAI")

if "state" not in st.session_state:
    st.session_state.state = None

if run_btn:
    with st.spinner("Running full AI pipeline..."):
        st.session_state.state = cached_engine(
            strategy, crew, productivity, curing
        )

state = st.session_state.state

if state is None:
    st.info("Configure parameters and run the engine.")
    st.stop()

if "error" in state:
    st.error(state["error"])
    st.stop()

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.title("STRUCTURA AI — Autonomous Construction Intelligence")

# ─────────────────────────────────────────────
# KPI BAR
# ─────────────────────────────────────────────
risk_matrix = state.get("risk_matrix", [])
avg_risk = round(sum(r["risk"] for r in risk_matrix)/len(risk_matrix), 1) if risk_matrix else 0

k1, k2, k3, k4 = st.columns(4)

k1.metric("AI Confidence", f"{state['detection_confidence']*100:.1f}%")
k2.metric("Duration (days)", state["execution_strategies"][state["strategy_selected"]]["duration_days"])
k3.metric("Buildability Score", state["execution_strategies"][state["strategy_selected"]]["buildability_score"])
k4.metric("Avg Risk Index", avg_risk)

st.divider()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Quantities & Cost", "Planning", "Intelligence"]
)

# ==========================================================
# OVERVIEW
# ==========================================================
with tab1:

    col1, col2 = st.columns([1,2])

    with col1:
        st.subheader("Strategy")
        st.write("Selected:", state["strategy_selected"])

        st.subheader("Executive Insight")
        ai = state["ai_explanation"]
        st.write("Summary:", ai["summary"])
        st.write("Risk Reasoning:", ai["risk_reasoning"])
        st.write("Recommendation:", ai["recommendation"])

    with col2:
        st.subheader("Digital Structural Twin")

        twin = state["digital_twin"]

        fig = go.Figure()

        for slab in twin.get("slabs", []):
            corners = slab.get("corners", [])
            if corners:
                xs = [pt[0] for pt in corners] + [corners[0][0]]
                ys = [pt[1] for pt in corners] + [corners[0][1]]
                fig.add_trace(go.Scatter(x=xs, y=ys, fill="toself"))

        for beam in twin.get("beams", []):
            s, e = beam["start"], beam["end"]
            fig.add_trace(go.Scatter(x=[s[0],e[0]], y=[s[1],e[1]]))

        for col in twin.get("columns", []):
            fig.add_trace(go.Scatter(
                x=[col["x"]], y=[col["y"]],
                mode="markers+text",
                text=[col["id"]]
            ))

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# QUANTITIES
# ==========================================================
with tab2:

    st.subheader("Bill of Quantities")
    df_qty = pd.DataFrame(state["quantity_takeoff"])
    st.dataframe(df_qty, use_container_width=True)

    st.subheader("Cost Breakdown")

    cost = state["cost_estimation"]
    if "phase_costs" in cost:
        df_cost = pd.DataFrame(cost["phase_costs"])
        fig_cost = px.bar(df_cost, x="phase", y="cost")
        st.plotly_chart(fig_cost, use_container_width=True)

# ==========================================================
# PLANNING
# ==========================================================
with tab3:

    st.subheader("Schedule")

    schedule = state["schedule"]
    if schedule:
        df_sched = pd.DataFrame(schedule)
        fig_gantt = px.timeline(df_sched,
            x_start="start", x_end="finish",
            y="task"
        )
        fig_gantt.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_gantt, use_container_width=True)

    st.subheader("Dependency Graph")

    graph_data = state["dependency_graph"]
    G = nx.DiGraph()
    G.add_nodes_from(graph_data["nodes"])
    G.add_edges_from(graph_data["edges"])

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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines"))
    fig.add_trace(go.Scatter(x=node_x, y=node_y,
                             mode="markers+text",
                             text=list(G.nodes())))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# INTELLIGENCE
# ==========================================================
with tab4:

    st.subheader("Conflicts")

    for c in state["conflicts"]:
        st.warning(f"{c['type']}: {c['description']}")

    st.subheader("Risk Matrix")

    df_risk = pd.DataFrame(state["risk_matrix"])
    fig_risk = px.bar(df_risk, x="phase", y="risk")
    st.plotly_chart(fig_risk, use_container_width=True)