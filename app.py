import streamlit as st
import plotly.express as px
import pandas as pd
import tempfile

from core.pipeline.analyzer import analyze_project
from core.pipeline.streamlit_adapter import adapt_to_dashboard_schema

st.set_page_config(layout="wide")
st.title("StructuraAI — Construction Intelligence Dashboard")

# ─────────────────────────────────────────
# Blueprint Type Selection
# ─────────────────────────────────────────
blueprint_type = st.radio(
    "Project Type",
    ["Residential Building", "Commercial Complex", "Industrial Facility"],
    horizontal=True
)

st.caption(f"Selected: {blueprint_type}")

uploaded_file = st.file_uploader(
    "Upload Project Blueprint (PDF)",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Analyzing structural drawing..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        raw_result = analyze_project(tmp_path, project_type=blueprint_type)

        if "error" in raw_result:
            st.error(raw_result["error"])
            st.stop()

        data = adapt_to_dashboard_schema(raw_result)

    # ─────────────────────────────────────────
    # Core Metrics
    # ─────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Detection Accuracy", f"{round(data['detection_confidence']*100,2)}%")
    col2.metric("Estimated Duration (days)", data["adjusted_metrics"]["duration"])
    col3.metric("Structural Efficiency", data["adjusted_metrics"]["buildability"])
    col4.metric("Overall Risk Index", round(data["adjusted_metrics"]["risk"],2))

    st.divider()

    # ─────────────────────────────────────────
    # What-If Simulation
    # ─────────────────────────────────────────
    st.subheader("Scenario Simulation")

    labor = st.slider("Available Workforce", 5, 100, 20)
    delay = st.slider("Material Delay (days)", 0, 60, 5)
    budget_factor = st.slider("Budget Flexibility", 0.8, 1.5, 1.0)

    adjusted_duration = int(data["adjusted_metrics"]["duration"] * (1 + delay/100))
    adjusted_cost = data["cost_estimation"]["total_project_cost"] * budget_factor
    adjusted_risk = min(100, data["adjusted_metrics"]["risk"] + delay*0.3)

    colA, colB, colC = st.columns(3)
    colA.metric("Revised Duration", adjusted_duration)
    colB.metric("Revised Budget", f"₹{adjusted_cost:,.0f}")
    colC.metric("Revised Risk", round(adjusted_risk,2))

    st.divider()

    # ─────────────────────────────────────────
    # Risk Breakdown
    # ─────────────────────────────────────────
    st.subheader("Risk Overview")

    if data["risk_matrix"]:
        df_risk = pd.DataFrame(data["risk_matrix"])

        fig = px.bar(
            df_risk,
            x="phase",
            y="risk",
            color="risk",
            color_continuous_scale="Reds"
        )
        fig.update_layout(title="Risk by Project Phase")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No risk data available.")

    st.divider()

    # ─────────────────────────────────────────
    # Gantt Schedule
    # ─────────────────────────────────────────
    st.subheader("Project Timeline")

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
        fig.update_layout(title="Execution Schedule")

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ─────────────────────────────────────────
    # PDF Download
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
    st.info("Upload a blueprint to begin analysis.")