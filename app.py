import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import tempfile

# Backend imports
from core.pipeline.analyzer import analyze_project
from core.pipeline.streamlit_adapter import adapt_to_dashboard_schema

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    layout="wide",
    page_title="StructuraAI — Command Center",
    page_icon="🏗️"
)

st.title("🏗️ StructuraAI — Construction Intelligence Command Center")
st.caption("AI-Powered Structural Analysis | Scheduling | Risk | Buildability")

# ============================================================
# SIDEBAR — WHAT IF CONTROLS
# ============================================================

st.sidebar.header("🔧 What-If Simulation Controls")

crew_capacity = st.sidebar.slider("Crew Capacity", 1, 10, 2)
productivity_factor = st.sidebar.slider("Productivity Factor", 0.5, 2.0, 1.0)
curing_days = st.sidebar.slider("Curing Days", 1, 7, 2)

st.sidebar.divider()

selected_strategy = st.sidebar.selectbox(
    "Execution Strategy",
    ["Baseline", "Fast Track", "Cost Optimized"]
)

# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload Civil Drawing (PDF)",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Analyzing blueprint and generating structural intelligence..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Pass dynamic simulation parameters to backend
        raw_result = analyze_project(
            tmp_path,
            crew_capacity=crew_capacity,
            productivity_factor=productivity_factor,
            curing_days=curing_days,
            strategy=selected_strategy
        )

        if "error" in raw_result:
            st.error(raw_result["error"])
            st.stop()

        data = adapt_to_dashboard_schema(raw_result)

    # ============================================================
    # EXECUTIVE KPI SECTION
    # ============================================================

    st.markdown("## 📊 Executive Metrics")

    risk_score = raw_result["risk"]["risk_score"]
    build_score = raw_result["buildability"]["final_score"]

    def risk_color(score):
        if score < 40:
            return "green"
        elif score < 70:
            return "orange"
        else:
            return "red"

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Detection Confidence",
        f"{round(data['detection_confidence'] * 100, 2)}%"
    )

    col2.metric(
        "Project Duration (Days)",
        data["adjusted_metrics"]["duration"]
    )

    col3.markdown(
        f"<h3 style='color:{risk_color(risk_score)}'>Risk Score: {risk_score}</h3>",
        unsafe_allow_html=True
    )

    col4.markdown(
        f"<h3 style='color:{risk_color(100 - build_score)}'>Buildability: {build_score}</h3>",
        unsafe_allow_html=True
    )

    st.divider()

    # ============================================================
    # RISK GAUGE
    # ============================================================

    st.subheader("🚨 Overall Risk Gauge")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={'text': "Project Risk"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': risk_color(risk_score)},
            'steps': [
                {'range': [0, 40], 'color': "green"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "red"}
            ],
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

    st.divider()

    # ============================================================
    # QUANTITY TAKEOFF
    # ============================================================

    st.subheader("📦 Quantity Takeoff")

    if data["quantity_takeoff"]:
        df_qto = pd.DataFrame(data["quantity_takeoff"])
        st.dataframe(df_qto, use_container_width=True)
    else:
        st.info("No quantity data available.")

    st.divider()

    # ============================================================
    # COST ESTIMATION
    # ============================================================

    st.subheader("💰 Cost Estimation")

    total_cost = data["cost_estimation"]["total_project_cost"]
    st.metric("Total Project Cost", f"₹{total_cost:,.0f}")

    if "phase_costs" in data["cost_estimation"]:
        df_cost = pd.DataFrame(data["cost_estimation"]["phase_costs"])
        fig_cost = px.bar(df_cost, x="phase", y="cost", title="Phase Cost Distribution")
        st.plotly_chart(fig_cost, use_container_width=True)

    st.divider()

    # ============================================================
    # SCHEDULE (GANTT)
    # ============================================================

    st.subheader("📅 Project Schedule")

    if data["schedule"]:
        df_schedule = pd.DataFrame(data["schedule"])
        df_schedule["start"] = pd.to_datetime(df_schedule["start"])
        df_schedule["finish"] = pd.to_datetime(df_schedule["finish"])

        fig_schedule = px.timeline(
            df_schedule,
            x_start="start",
            x_end="finish",
            y="task"
        )

        fig_schedule.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_schedule, use_container_width=True)
    else:
        st.info("No schedule data available.")

    st.divider()

    # ============================================================
    # STRATEGY COMPARISON
    # ============================================================

    st.subheader("⚡ Strategy Comparison")

    baseline_duration = data["adjusted_metrics"]["duration"]
    fast_track = int(baseline_duration * 0.9)
    cost_opt = int(baseline_duration * 1.1)

    df_strategy = pd.DataFrame({
        "Strategy": ["Baseline", "Fast Track", "Cost Optimized"],
        "Duration": [baseline_duration, fast_track, cost_opt]
    })

    fig_strategy = px.bar(df_strategy, x="Strategy", y="Duration")
    st.plotly_chart(fig_strategy, use_container_width=True)

    st.divider()

    # ============================================================
    # RISK MATRIX
    # ============================================================

    st.subheader("📊 Risk Matrix")

    if data["risk_matrix"]:
        df_risk = pd.DataFrame(data["risk_matrix"])
        fig_risk = px.bar(
            df_risk,
            x="phase",
            y="risk",
            color="risk",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    else:
        st.info("No risk data available.")

    st.divider()

    # ============================================================
    # CONFLICTS
    # ============================================================

    st.subheader("⚠️ Detected Conflicts")

    if data["conflicts"]:
        for c in data["conflicts"]:
            st.warning(f"{c['type']}: {c['description']}")
    else:
        st.success("No conflicts detected.")

    st.divider()

    # ============================================================
    # DIGITAL TWIN
    # ============================================================

    st.subheader("🏗️ Digital Structural Twin")

    if "walls" in raw_result["twin"]:
        st.json(raw_result["twin"])
    else:
        st.info("No structural twin data available.")

    st.divider()

    # ============================================================
    # AI EXPLANATION
    # ============================================================

    st.subheader("🧠 AI Strategic Explanation")

    st.write(data["ai_explanation"]["summary"])
    st.write("Risk Reasoning:", data["ai_explanation"]["risk_reasoning"])
    st.write("Recommendation:", data["ai_explanation"]["recommendation"])

    st.divider()

    # ============================================================
    # PDF DOWNLOAD
    # ============================================================

    if "pdf_path" in raw_result:
        with open(raw_result["pdf_path"], "rb") as f:
            st.download_button(
                label="📄 Download Full Project Report (PDF)",
                data=f,
                file_name="structuraai_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("Upload a blueprint PDF to begin analysis.")