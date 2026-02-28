import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
from PIL import Image
from datetime import datetime
import random

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(layout="wide", page_title="StructuraAI", page_icon="🏗️")

# ============================================
# DESIGN TOKENS
# ============================================

BG = "#0F172A"
CARD = "#1E293B"
BORDER = "#334155"
PRIMARY = "#6366F1"
CYAN = "#22D3EE"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
TEXT = "#E2E8F0"
MUTED = "#94A3B8"

st.markdown(f"""
<style>
body {{ background:{BG}; color:{TEXT}; }}
.block-container {{ padding:2rem 3rem; }}
.metric-card {{
    background:{CARD};
    padding:20px;
    border-radius:16px;
    border:1px solid {BORDER};
}}
.section-card {{
    background:{CARD};
    padding:24px;
    border-radius:18px;
    border:1px solid {BORDER};
    margin-bottom:24px;
}}
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================

with open("data/project_state.json") as f:
    state = json.load(f)

risk_matrix = state["risk_matrix"]
schedule = state["schedule"]
cost = state["cost_estimation"]
strategies = state["execution_strategies"]
selected = state["strategy_selected"]
twin = state["digital_twin"]

# ============================================
# HEADER
# ============================================

st.title("StructuraAI — Autonomous Construction Intelligence")

# ============================================
# KPI GRID WITH SPARKLINES
# ============================================

def sparkline(base):
    values = [base + random.randint(-3,3) for _ in range(10)]
    fig = go.Figure(go.Scatter(y=values, mode="lines",
                               line=dict(color=PRIMARY,width=2)))
    fig.update_layout(height=60, margin=dict(l=0,r=0,t=0,b=0),
                      plot_bgcolor=CARD, paper_bgcolor=CARD,
                      xaxis=dict(visible=False),
                      yaxis=dict(visible=False))
    return fig

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    conf = state["detection_confidence"]*100
    st.metric("AI Confidence", f"{conf:.1f}%")
    st.plotly_chart(sparkline(int(conf)),use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    total_cost = cost["total_project_cost"]
    st.metric("Total Cost", f"₹ {total_cost:,}")
    st.plotly_chart(sparkline(total_cost//1000000),use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    build = strategies[selected]["buildability_score"]
    st.metric("Buildability", build)
    st.plotly_chart(sparkline(build),use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    avg_risk = round(sum(r["risk"] for r in risk_matrix)/len(risk_matrix),1)
    st.metric("Risk Index", f"{avg_risk}/5")
    st.plotly_chart(sparkline(int(avg_risk*10)),use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# PROFESSIONAL GAUGE METER
# ============================================

left,right = st.columns(2)

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=build,
        gauge={
            "axis": {"range":[0,100]},
            "bar": {"color":PRIMARY},
            "steps":[
                {"range":[0,40],"color":DANGER},
                {"range":[40,70],"color":WARNING},
                {"range":[70,100],"color":SUCCESS}
            ]
        }
    ))
    fig_gauge.update_layout(height=300,paper_bgcolor=CARD,font=dict(color=TEXT))
    st.subheader("Buildability Score")
    st.plotly_chart(fig_gauge,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    fig_gauge2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk,
        gauge={
            "axis": {"range":[0,5]},
            "bar": {"color":DANGER},
            "steps":[
                {"range":[0,2],"color":SUCCESS},
                {"range":[2,4],"color":WARNING},
                {"range":[4,5],"color":DANGER}
            ]
        }
    ))
    fig_gauge2.update_layout(height=300,paper_bgcolor=CARD,font=dict(color=TEXT))
    st.subheader("Risk Gauge")
    st.plotly_chart(fig_gauge2,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# BLUEPRINT OVERLAY DIGITAL TWIN
# ============================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Blueprint Overlay + Structural Twin")

uploaded = st.file_uploader("Upload Blueprint Image (for overlay)",type=["png","jpg","jpeg"])

fig_overlay = go.Figure()

if uploaded:
    image = Image.open(uploaded)
    fig_overlay.add_layout_image(
        dict(
            source=image,
            x=0,
            y=0,
            sizex=20,
            sizey=20,
            xref="x",
            yref="y",
            opacity=0.6,
            layer="below"
        )
    )

for beam in twin["beams"]:
    fig_overlay.add_trace(go.Scatter(
        x=[beam["start"][0],beam["end"][0]],
        y=[beam["start"][1],beam["end"][1]],
        mode="lines",
        line=dict(width=4,color=PRIMARY)
    ))

for col in twin["columns"]:
    fig_overlay.add_trace(go.Scatter(
        x=[col["x"]],
        y=[col["y"]],
        mode="markers",
        marker=dict(size=14,color=CYAN)
    ))

fig_overlay.update_layout(
    plot_bgcolor=CARD,
    paper_bgcolor=CARD,
    height=500,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)

st.plotly_chart(fig_overlay,use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ANIMATED GANTT
# ============================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Execution Timeline")

df_s = pd.DataFrame(schedule)

fig_timeline = px.timeline(
    df_s,
    x_start="start",
    x_end="finish",
    y="task",
    color="task"
)

fig_timeline.update_layout(
    plot_bgcolor=CARD,
    paper_bgcolor=CARD,
    font=dict(color=TEXT),
    showlegend=False,
    height=350,
    transition_duration=800
)

fig_timeline.update_yaxes(autorange="reversed")

st.plotly_chart(fig_timeline,use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)