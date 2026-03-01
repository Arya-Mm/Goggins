import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
import tempfile

# Backend imports
from core.pipeline.analyzer import analyze_project
from core.pipeline.streamlit_adapter import adapt_to_dashboard_schema

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="StructuraAI — Command Center",
    page_icon="🏗️"
)

st.title("🏗️ StructuraAI Command Center")

# ─────────────────────────────────────────────
# FILE UPLOAD
# ─────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload Civil Drawing (PDF)",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Analyzing blueprint..."):

        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Run backend engine
        raw_result = analyze_project(tmp_path)

        if "error" in raw_result:
            st.error(raw_result["error"])
            st.stop()

        # Adapt schema for dashboard
        data = adapt_to_dashboard_schema(raw_result)

    # ─────────────────────────────────────────
    # KPI SECTION
    # ─────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Detection Confidence",
        f"{round(data['detection_confidence'] * 100, 2)}%"
    )

    col2.metric(
        "Project Duration (Days)",
        data["adjusted_metrics"]["duration"]
    )

    col3.metric(
        "Buildability Score",
        data["adjusted_metrics"]["buildability"]
    )

    col4.metric(
        "Risk Index",
        round(data["adjusted_metrics"]["risk"], 2)
    )

    st.divider()

    # ─────────────────────────────────────────
    # QUANTITY TAKEOFF
    # ─────────────────────────────────────────
    st.subheader("Quantity Takeoff")

    if data["quantity_takeoff"]:
        df_qto = pd.DataFrame(data["quantity_takeoff"])
        st.dataframe(df_qto, use_container_width=True)
    else:
        st.info("No quantity data available.")

    st.divider()

    # ─────────────────────────────────────────
    # COST ESTIMATION
    # ─────────────────────────────────────────
    st.subheader("Cost Estimation")

    total_cost = data["cost_estimation"]["total_project_cost"]
    st.metric("Total Project Cost", f"₹{total_cost:,.0f}")

    st.divider()

    # ─────────────────────────────────────────
    # SCHEDULE GANTT
    # ─────────────────────────────────────────
    st.subheader("Project Schedule")

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
    else:
        st.info("No schedule data available.")

    st.divider()

    # ─────────────────────────────────────────
    # RISK MATRIX
    # ─────────────────────────────────────────
    st.subheader("Risk Matrix")

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

    # ─────────────────────────────────────────
    # CONFLICTS
    # ─────────────────────────────────────────
    st.subheader("Detected Conflicts")

    if data["conflicts"]:
        for c in data["conflicts"]:
            st.warning(f"{c['type']}: {c['description']}")
    else:
        st.success("No conflicts detected.")

    st.divider()

    # ─────────────────────────────────────────
    # AI EXPLANATION
    # ─────────────────────────────────────────
    st.subheader("AI Strategic Explanation")

    st.write(data["ai_explanation"]["summary"])
    st.write("Risk Reasoning:", data["ai_explanation"]["risk_reasoning"])
    st.write("Recommendation:", data["ai_explanation"]["recommendation"])

    st.divider()

    # ─────────────────────────────────────────
    # PDF DOWNLOAD
    # ─────────────────────────────────────────
    if "pdf_path" in raw_result:
        with open(raw_result["pdf_path"], "rb") as f:
            st.download_button(
                label="Download Full Project Report (PDF)",
                data=f,
                file_name="structuraai_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("Upload a blueprint PDF to begin analysis.")