import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.twin.twin_builder import build_structural_twin

# Page Config
st.set_page_config(layout="wide")

st.title("StructuraAI – Autonomous Pre-Construction Intelligence")

st.markdown("Upload a civil engineering blueprint to generate execution intelligence.")

uploaded_file = st.file_uploader("Upload Blueprint", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:

    st.success("Blueprint uploaded successfully.")

    # =============================
    # DIGITAL STRUCTURAL TWIN
    # =============================
    twin_obj = build_structural_twin()
    twin = twin_obj.to_dict()

    st.subheader("Digital Structural Twin")
    col1, col2, col3 = st.columns(3)

    col1.metric("Columns", twin["columns"])
    col2.metric("Beams", twin["beams"])
    col3.metric("Slabs", twin["slabs"])

    # =============================
    # EXECUTION STRATEGY (TEMP)
    # =============================
    strategy_type = "Balanced"
    estimated_duration = 120

    st.subheader("Execution Strategy")
    st.write(f"Strategy Type: **{strategy_type}**")
    st.write(f"Estimated Duration: **{estimated_duration} days**")

    # =============================
    # BUILDABILITY SCORE (TEMP)
    # =============================
    buildability_score = 82

    st.subheader("Buildability Score")
    st.metric("Score", f"{buildability_score} / 100")

    # =============================
    # AI INSIGHT (TEMP EXPLANATION)
    # =============================
    st.subheader("AI Insight")
    st.info(
        "Balanced strategy minimizes concurrency risk while maintaining steady structural progression."
    )

else:
    st.info("Please upload a blueprint to begin.")