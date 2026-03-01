import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
from main import run_engine
from core.exports.pdf_report import generate_pdf_report

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="StructuraAI — AI Construction Intelligence",
)

# ─────────────────────────────────────────────
# CUSTOM CSS (Minimal / Premium)
# ─────────────────────────────────────────────
st.markdown("""
<style>
body { background-color: #0E1117; }
.metric-card {
    background-color: #1C1F26;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2A2E39;
}
</style>
""", unsafe_allow_html=True)

st.title("🏗 StructuraAI — Autonomous Construction Intelligence")

# ─────────────────────────────────────────────
# STRATEGY SELECTION
# ─────────────────────────────────────────────
strategy = st.radio(
    "Select Construction Strategy",
    ["Balanced", "FastTrack", "CostOptimized"],
    horizontal=True
)

# ─────────────────────────────────────────────
# WHAT-IF SIMULATION POPUP
# ─────────────────────────────────────────────
with st.expander("⚙ What-If Simulation Layer"):

    crew_capacity = st.slider("Crew Capacity", 1, 10, 2)
    productivity = st.slider("Productivity Factor", 0.5, 2.0, 1.0)
    curing_days = st.slider("Curing Days", 1, 7, 2)

    run_simulation = st.button("Run What-If Scenario")

# ─────────────────────────────────────────────
# RUN ENGINE
# ─────────────────────────────────────────────
with st.spinner("Running AI Construction Engine..."):

    result = run_engine(
        strategy=strategy,
        crew_capacity=crew_capacity,
        productivity_factor=productivity,
        curing_days=curing_days
    )

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Duration (Days)", result["duration"])
col2.metric("Buildability", round(result["buildability"]["final_score"], 2))
col3.metric("Risk Score", round(result["risk"]["risk_score"], 2))
col4.metric("Strategy", strategy)

st.divider()

# ─────────────────────────────────────────────
# GAUGE
# ─────────────────────────────────────────────
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=result["buildability"]["final_score"],
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#00D084"},
        "steps": [
            {"range": [0, 40], "color": "#FF4B4B"},
            {"range": [40, 70], "color": "#FFA500"},
            {"range": [70, 100], "color": "#00D084"},
        ],
    }
))
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# GANTT CHART
# ─────────────────────────────────────────────
st.subheader("📅 Construction Timeline")

schedule_data = []

G = result["graph"]

for node in G.nodes:
    if "ES" in G.nodes[node] and "EF" in G.nodes[node]:
        schedule_data.append({
            "Task": node,
            "Start": G.nodes[node]["ES"],
            "Finish": G.nodes[node]["EF"]
        })

df = pd.DataFrame(schedule_data)

fig_gantt = px.timeline(
    df,
    x_start="Start",
    x_end="Finish",
    y="Task"
)

fig_gantt.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig_gantt, use_container_width=True)

# ─────────────────────────────────────────────
# RISK DIAGRAM
# ─────────────────────────────────────────────
st.subheader("⚠ Risk Breakdown")

risk_df = pd.DataFrame([
    result["risk"]["breakdown"]
]).T.reset_index()

risk_df.columns = ["Factor", "Score"]

fig_risk = px.bar(
    risk_df,
    x="Factor",
    y="Score",
    color="Score",
    color_continuous_scale="Reds"
)

fig_risk.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig_risk, use_container_width=True)

# ─────────────────────────────────────────────
# AI EXPLANATION
# ─────────────────────────────────────────────
st.subheader("🧠 AI Construction Intelligence")

st.write(result["ai_explanation"])

st.divider()

# ─────────────────────────────────────────────
# PDF GENERATION
# ─────────────────────────────────────────────
if st.button("📄 Generate Investor-Grade PDF Report"):

    pdf_path = generate_pdf_report(result["pdf_data"])

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download Report",
            data=f,
            file_name="StructuraAI_Report.pdf",
            mime="application/pdf"
        )