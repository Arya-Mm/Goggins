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
st.set_page_config(
    layout="wide",
    page_title="StructuraAI",
    page_icon="◈",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ─── DESIGN TOKENS ─── */
:root {
    --bg:             #EEF0F8;
    --glass:          rgba(255,255,255,0.64);
    --glass-2:        rgba(255,255,255,0.40);
    --glass-border:   rgba(255,255,255,0.90);
    --glass-border-2: rgba(255,255,255,0.50);
    --shadow:         0 8px 32px rgba(50,70,130,0.10), 0 1.5px 5px rgba(50,70,130,0.06);
    --shadow-hover:   0 18px 52px rgba(50,70,130,0.16), 0 3px 10px rgba(50,70,130,0.08);
    --blur:           saturate(180%) blur(22px);
    --blur-sm:        saturate(160%) blur(12px);
    --accent:         #007AFF;
    --accent-2:       #5856D6;
    --accent-soft:    rgba(0,122,255,0.10);
    --accent-glow:    rgba(0,122,255,0.22);
    --text:           #1C1C2E;
    --text-2:         #556070;
    --muted:          #99A0AE;
    --r-xl:           22px;
    --r-lg:           16px;
    --r-md:           12px;
    --r-pill:         999px;
}

/* ─── BASE ─── */
html, body, [class*="css"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    letter-spacing: -0.01em;
}

.stApp {
    background:
        radial-gradient(ellipse 70% 55% at 12% 8%,  rgba(0,122,255,0.11) 0%, transparent 58%),
        radial-gradient(ellipse 55% 50% at 88% 85%,  rgba(88,86,214,0.09) 0%, transparent 55%),
        radial-gradient(ellipse 65% 60% at 55% 45%,  rgba(255,255,255,0.55) 0%, transparent 65%),
        linear-gradient(155deg, #E9ECF7 0%, #F4F5FB 45%, #EBEDf7 100%) !important;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 2.8rem 3.6rem !important; max-width: 1380px !important; }

/* ─── NAV ─── */
.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}
.brand { display: flex; align-items: center; gap: 0.85rem; }
.mark {
    width: 42px; height: 42px;
    background: linear-gradient(140deg, #007AFF 0%, #5856D6 100%);
    border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.15rem; font-weight: 700;
    box-shadow: 0 5px 18px rgba(0,122,255,0.38);
    letter-spacing: -0.05em;
}
.wordmark {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.6rem;
    letter-spacing: -0.045em;
    color: var(--text);
    line-height: 1;
}
.wordmark em { color: var(--accent); font-style: normal; }
.tagline {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.20em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 2px;
}
.badge {
    background: var(--glass);
    backdrop-filter: var(--blur-sm);
    -webkit-backdrop-filter: var(--blur-sm);
    border: 1px solid var(--glass-border);
    border-radius: var(--r-pill);
    padding: 0.38rem 1.05rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    box-shadow: var(--shadow);
}

/* ─── SECTION LABEL ─── */
.sl {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 2.6rem 0 1.05rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.sl::before {
    content: '';
    width: 14px; height: 1.5px;
    background: var(--accent);
    border-radius: 2px;
}
.sl::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(0,122,255,0.18), transparent);
}

/* ─── STRATEGY PILLS ─── */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 0.5rem !important;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] label {
    background: var(--glass-2) !important;
    backdrop-filter: var(--blur-sm) !important;
    -webkit-backdrop-filter: var(--blur-sm) !important;
    border: 1px solid var(--glass-border-2) !important;
    border-radius: var(--r-pill) !important;
    padding: 0.48rem 1.3rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: var(--text-2) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 6px rgba(50,70,130,0.06) !important;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.78) !important;
    border-color: rgba(0,122,255,0.28) !important;
    color: var(--accent) !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 18px rgba(0,122,255,0.35) !important;
}

/* ─── STRATEGY STRIP ─── */
.strat {
    background: var(--glass-2);
    backdrop-filter: var(--blur-sm);
    -webkit-backdrop-filter: var(--blur-sm);
    border: 1px solid var(--glass-border-2);
    border-left: 3px solid var(--accent);
    border-radius: var(--r-lg);
    padding: 0.85rem 1.3rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-2);
    line-height: 1.75;
    margin-top: 0.65rem;
    box-shadow: 0 2px 10px rgba(0,122,255,0.06);
}
.strat b { color: var(--accent); font-weight: 700; }

/* ─── FILE UPLOADER ─── */
[data-testid="stFileUploader"] {
    background: var(--glass) !important;
    backdrop-filter: var(--blur) !important;
    -webkit-backdrop-filter: var(--blur) !important;
    border: 1.5px dashed rgba(0,122,255,0.30) !important;
    border-radius: var(--r-xl) !important;
    box-shadow: var(--shadow) !important;
    transition: all 0.22s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--accent-glow), var(--shadow) !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; }

/* ─── METRIC CARDS ─── */
[data-testid="metric-container"] {
    background: var(--glass) !important;
    backdrop-filter: var(--blur) !important;
    -webkit-backdrop-filter: var(--blur) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--r-xl) !important;
    padding: 1.5rem 1.65rem 1.4rem !important;
    box-shadow: var(--shadow) !important;
    transition: all 0.25s ease !important;
}
[data-testid="metric-container"]:hover {
    box-shadow: var(--shadow-hover) !important;
    transform: translateY(-3px) !important;
    border-color: rgba(0,122,255,0.28) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.58rem !important;
    letter-spacing: 0.20em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 400 !important;
    margin-bottom: 0.35rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -0.04em !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }
[data-testid="stMetricDelta"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    margin-top: 0.3rem !important;
}

/* ─── SLIDERS ─── */
.stSlider > label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 400 !important;
}

/* ─── CHECKBOX ─── */
.stCheckbox label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.83rem !important;
    color: var(--text-2) !important;
    font-weight: 500 !important;
}

/* ─── CAPTION ─── */
[data-testid="caption"], .stCaption {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.67rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.03em !important;
}

/* ─── DIVIDER ─── */
hr {
    border: none !important;
    border-top: 1px solid rgba(0,122,255,0.09) !important;
    margin: 0.3rem 0 !important;
}

/* ─── ALERTS ─── */
.stAlert {
    background: var(--glass) !important;
    backdrop-filter: var(--blur) !important;
    -webkit-backdrop-filter: var(--blur) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--r-lg) !important;
    box-shadow: var(--shadow) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--text-2) !important;
}

/* ─── DOWNLOAD BUTTON ─── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--r-pill) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.87rem !important;
    padding: 0.72rem 2.3rem !important;
    box-shadow: 0 5px 22px rgba(0,122,255,0.38) !important;
    transition: all 0.22s ease !important;
    letter-spacing: -0.01em !important;
}
.stDownloadButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(0,122,255,0.48) !important;
}

/* ─── SPINNER ─── */
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)

# ── Navbar ─────────────────────────────────
st.markdown("""
<div class="nav">
  <div class="brand">
    <div class="mark">◈</div>
    <div>
      <div class="wordmark">Structura<em>AI</em></div>
      <div class="tagline">Construction Intelligence Platform</div>
    </div>
  </div>
  <div class="badge">v2.0 · Professional</div>
</div>
""", unsafe_allow_html=True)

# ── Strategy ────────────────────────────────
st.markdown('<div class="sl">Execution Strategy</div>', unsafe_allow_html=True)

strategy = st.radio("", ["Cost Optimized", "Balanced", "Fast Track"],
                    horizontal=True, label_visibility="collapsed")

info = {
    "Cost Optimized": "<b>Cost Optimized</b> &nbsp;·&nbsp; Reduced crew size and extended schedule. 5% budget reduction.",
    "Balanced":       "<b>Balanced</b> &nbsp;·&nbsp; Baseline crew, schedule, and cost. Recommended starting point.",
    "Fast Track":     "<b>Fast Track</b> &nbsp;·&nbsp; Maximum parallelism, compressed schedule. 10% cost premium.",
}
st.markdown(f'<div class="strat">{info[strategy]}</div>', unsafe_allow_html=True)

if strategy == "Cost Optimized":
    df_, cf_ = 1.15, 0.95
elif strategy == "Fast Track":
    df_, cf_ = 0.85, 1.10
else:
    df_, cf_ = 1.0, 1.0

# ── Upload ──────────────────────────────────
st.markdown('<div class="sl">Blueprint Upload</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop structural blueprint PDF here — or click to browse",
    type=["pdf"], label_visibility="visible"
)

# ── Processing ──────────────────────────────
if uploaded_file:

    with st.spinner("Parsing structural blueprint…"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        raw_result = analyze_project(tmp_path)
        if "error" in raw_result:
            st.error(raw_result["error"]); st.stop()

        data = adapt_to_dashboard_schema(raw_result)

    base_duration = data["adjusted_metrics"]["duration"]
    base_cost     = data["cost_estimation"]["total_project_cost"]
    base_risk     = data["adjusted_metrics"]["risk"]
    base_build    = data["adjusted_metrics"]["buildability"]
    strat_dur     = int(base_duration * df_)
    strat_cost    = base_cost * cf_

    # Overview
    st.markdown('<div class="sl">Project Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Detection Confidence", f"{round(data['detection_confidence']*100,2)}%")
    c2.metric("Planned Duration",     f"{strat_dur}d")
    c3.metric("Estimated Budget",     f"₹{strat_cost:,.0f}")
    c4.metric("Buildability Score",   base_build)

    st.markdown("---")

    # Scenario
    st.markdown('<div class="sl">Scenario Simulation</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1: labor_d  = st.slider("Workforce Adjustment (%)", -50, 50, 0)
    with s2: delay_d  = st.slider("Material Delay (days)", -30, 60, 0)
    with s3: budget_d = st.slider("Budget Adjustment (%)", -30, 50, 0)

    rev_dur  = int(strat_dur  * (1 - labor_d / 100) + delay_d)
    rev_cost = strat_cost * (1 + budget_d / 100)
    rev_risk = max(0, min(100, base_risk + delay_d * 0.4 - labor_d * 0.2))

    r1, r2, r3 = st.columns(3)
    r1.metric("Revised Duration",   f"{rev_dur}d",          delta=f"{rev_dur  - strat_dur:+d}d")
    r2.metric("Revised Budget",     f"₹{rev_cost:,.0f}",   delta=f"₹{rev_cost - strat_cost:+,.0f}")
    r3.metric("Revised Risk Index", round(rev_risk, 2),     delta=f"{round(rev_risk - base_risk, 2):+.2f}")

    st.markdown("---")

    # Graph
    PLOT_BG = "rgba(255,255,255,0.58)"
    st.markdown('<div class="sl">Execution Network</div>', unsafe_allow_html=True)

    graph_data    = data.get("dependency_graph", {})
    critical_path = data.get("critical_path", [])
    highlight_only = st.checkbox("Show critical path only")

    if graph_data:
        G = nx.DiGraph()
        G.add_nodes_from(graph_data["nodes"])
        G.add_edges_from(graph_data["edges"])
        pos = nx.spring_layout(G, k=0.9, iterations=120, seed=42)

        edge_x, edge_y, crit_x, crit_y = [], [], [], []
        for e in G.edges():
            x0, y0 = pos[e[0]]; x1, y1 = pos[e[1]]
            if e[0] in critical_path and e[1] in critical_path:
                crit_x += [x0,x1,None]; crit_y += [y0,y1,None]
            elif not highlight_only:
                edge_x += [x0,x1,None]; edge_y += [y0,y1,None]

        traces = []
        if edge_x:
            traces.append(go.Scatter(x=edge_x, y=edge_y, mode="lines",
                line=dict(width=1, color="rgba(0,122,255,0.13)"), hoverinfo="none"))
        if crit_x:
            traces.append(go.Scatter(x=crit_x, y=crit_y, mode="lines",
                line=dict(width=2.8, color="rgba(0,122,255,0.72)"), hoverinfo="none"))

        nx_, ny_, nt_, nc_, nb_ = [], [], [], [], []
        for node in G.nodes():
            x, y = pos[node]
            nx_.append(x); ny_.append(y); nt_.append(node)
            if node in critical_path:
                nc_.append("#007AFF"); nb_.append("white")
            else:
                nc_.append("rgba(255,255,255,0.85)"); nb_.append("rgba(0,122,255,0.28)")

        traces.append(go.Scatter(
            x=nx_, y=ny_, mode="markers+text",
            text=nt_, textposition="top center",
            textfont=dict(family="Space Mono", size=9, color="#556070"),
            marker=dict(size=26, color=nc_, line=dict(width=1.5, color=nb_)),
            hovertemplate="<b>%{text}</b><extra></extra>"
        ))

        fig_g = go.Figure(data=traces)
        fig_g.update_layout(height=480, plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            margin=dict(l=24,r=24,t=24,b=24), showlegend=False,
            xaxis=dict(showgrid=False,visible=False), yaxis=dict(showgrid=False,visible=False),
            font=dict(family="Space Grotesk"))
        st.plotly_chart(fig_g, use_container_width=True)
        st.caption("Blue-filled nodes and edges mark the critical path. Any delay there shifts your delivery date.")

    st.markdown("---")

    # Risk
    st.markdown('<div class="sl">Risk by Phase</div>', unsafe_allow_html=True)
    if data["risk_matrix"]:
        df_risk = pd.DataFrame(data["risk_matrix"])
        fig_r = px.bar(df_risk, x="phase", y="risk", color="risk",
            color_continuous_scale=[[0,"rgba(0,122,255,0.18)"],[0.5,"rgba(0,122,255,0.55)"],[1,"#007AFF"]])
        fig_r.update_layout(plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family="Space Grotesk", color="#99A0AE"),
            xaxis=dict(title=None, gridcolor="rgba(0,122,255,0.06)",
                tickfont=dict(family="Space Mono", size=9, color="#99A0AE"), linecolor="transparent"),
            yaxis=dict(title=None, gridcolor="rgba(0,122,255,0.06)",
                tickfont=dict(family="Space Mono", size=9, color="#99A0AE"), linecolor="transparent"),
            coloraxis_showscale=False, margin=dict(l=10,r=10,t=10,b=10), bargap=0.38)
        fig_r.update_traces(marker_line_width=0)
        st.plotly_chart(fig_r, use_container_width=True)

    st.markdown("---")

    # Timeline
    st.markdown('<div class="sl">Execution Timeline</div>', unsafe_allow_html=True)
    if data["schedule"]:
        df_s = pd.DataFrame(data["schedule"])
        df_s["start"]  = pd.to_datetime(df_s["start"])
        df_s["finish"] = pd.to_datetime(df_s["finish"])
        fig_t = px.timeline(df_s, x_start="start", x_end="finish", y="task",
            color_discrete_sequence=["#007AFF"])
        fig_t.update_yaxes(autorange="reversed")
        fig_t.update_layout(plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family="Space Grotesk", color="#99A0AE"),
            xaxis=dict(gridcolor="rgba(0,122,255,0.06)",
                tickfont=dict(family="Space Mono", size=9, color="#99A0AE"), linecolor="transparent"),
            yaxis=dict(gridcolor="rgba(0,122,255,0.06)",
                tickfont=dict(family="Space Mono", size=9, color="#99A0AE"), linecolor="transparent"),
            margin=dict(l=10,r=10,t=10,b=10))
        fig_t.update_traces(marker_line_width=0)
        st.plotly_chart(fig_t, use_container_width=True)

    st.markdown("---")

    # Export
    if "pdf_path" in raw_result:
        st.markdown('<div class="sl">Export</div>', unsafe_allow_html=True)
        with open(raw_result["pdf_path"], "rb") as f:
            st.download_button("↓  Download Intelligence Report", f,
                file_name="structuraai_report.pdf", mime="application/pdf")

else:
    st.markdown('<div class="sl">Get Started</div>', unsafe_allow_html=True)
    st.info("Upload a structural blueprint PDF above to begin analysis.")