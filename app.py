import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
import tempfile

from core.pipeline.analyzer import analyze_project
from core.pipeline.streamlit_adapter import adapt_to_dashboard_schema

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="StructuraAI",
    layout="wide",
    page_icon="🏗️"
)

# =========================================================
# ENTERPRISE DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>

body { background-color: #F5F7FA; }

.block-container {
    padding: 2rem 3rem;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

.section-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

h1 {
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("StructuraAI")

    strategy = st.radio(
        "Execution Strategy",
        ["Balanced", "Fast Track", "Cost Optimized"]
    )

    labor = st.slider("Labor Multiplier", 0.5, 2.0, 1.0)
    delay = st.slider("Material Delay (Days)", 0, 20, 0)

# =========================================================
# FILE UPLOAD
# =========================================================

st.title("Autonomous Construction Intelligence Platform")

uploaded = st.file_uploader("Upload Civil Drawing (PDF)", type=["pdf"])

if not uploaded:
    st.stop()

with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
    tmp.write(uploaded.read())
    tmp_path = tmp.name

raw = analyze_project(tmp_path)
data = adapt_to_dashboard_schema(raw)

# =========================================================
# STRATEGY EFFECT
# =========================================================

base_duration = data["adjusted_metrics"]["duration"]

if strategy == "Fast Track":
    duration = int(base_duration * 0.85)
elif strategy == "Cost Optimized":
    duration = int(base_duration * 1.15)
else:
    duration = base_duration

duration = int(duration / labor) + delay

# =========================================================
# KPI GRID
# =========================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Detection Confidence", f"{round(data['detection_confidence']*100,2)}%")
    st.markdown('</div>', unsafe_allow_html=True)

with k2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Duration (Days)", duration)
    st.markdown('</div>', unsafe_allow_html=True)

with k3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Buildability Score", data["adjusted_metrics"]["buildability"])
    st.markdown('</div>', unsafe_allow_html=True)

with k4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Risk Index", round(data["adjusted_metrics"]["risk"],2))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# ROW 1: SCHEDULE + RISK
# =========================================================

colA, colB = st.columns([2,1])

with colA:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Project Schedule")

    if data["schedule"]:
        df = pd.DataFrame(data["schedule"])
        df["start"] = pd.to_datetime(df["start"])
        df["finish"] = pd.to_datetime(df["finish"])

        fig = px.timeline(df, x_start="start", x_end="finish", y="task")
        fig.update_layout(height=350)
        fig.update_yaxes(autorange="reversed")

        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Risk Matrix")

    if data["risk_matrix"]:
        df_r = pd.DataFrame(data["risk_matrix"])
        fig_r = px.bar(df_r, x="phase", y="risk", color="risk")
        fig_r.update_layout(height=350)
        st.plotly_chart(fig_r, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ROW 2: DIGITAL TWIN + DEPENDENCY
# =========================================================

colC, colD = st.columns(2)

with colC:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Digital Structural Twin")

    twin = raw.get("twin", {})

    fig_twin = go.Figure()

    for wall in twin.get("walls", []):
        length = wall.get("length_inches", 100)
        fig_twin.add_trace(go.Scatter(
            x=[0, length],
            y=[0, 0],
            mode="lines",
            line=dict(width=6)
        ))

    fig_twin.update_layout(height=350)
    st.plotly_chart(fig_twin, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colD:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Dependency Graph")

    if "dependency_graph" in data:
        G = nx.DiGraph()
        G.add_edges_from(data["dependency_graph"]["edges"])

        pos = nx.spring_layout(G)

        edge_x, edge_y = [], []

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        fig_g = go.Figure()

        fig_g.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode="lines"
        ))

        node_x, node_y = [], []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        fig_g.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=list(G.nodes()),
            textposition="bottom center",
            marker=dict(size=18)
        ))

        fig_g.update_layout(height=350)
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# STRATEGY COMPARISON
# =========================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Strategy Comparison")

df_compare = pd.DataFrame({
    "Strategy": ["Balanced", "Fast Track", "Cost Optimized"],
    "Duration": [
        base_duration,
        int(base_duration*0.85),
        int(base_duration*1.15)
    ]
})

fig_c = px.bar(df_compare, x="Strategy", y="Duration")
st.plotly_chart(fig_c, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# AI SUMMARY
# =========================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("AI Strategic Report")

st.write(data["ai_explanation"]["summary"])
st.write("Risk Reasoning:", data["ai_explanation"]["risk_reasoning"])
st.write("Recommendation:", data["ai_explanation"]["recommendation"])

st.markdown('</div>', unsafe_allow_html=True)