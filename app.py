import streamlit as st
import pandas as pd

from governance_data import AI_SYSTEM_TYPES
from checklist_engine import (
    generate_checklist,
    calculate_risk_counts,
    calculate_governance_score,
    get_overall_governance_assessment
)


st.set_page_config(
    page_title="AI Governance Checklist Generator",
    layout="wide"
)


st.title("AI Governance Checklist Generator")

st.warning(
    "This public demo is for educational and portfolio purposes only. "
    "It does not provide legal advice or regulatory compliance certification. "
    "Do not enter confidential, personal, sensitive or proprietary information."
)

st.caption(
    "A rule-based AI governance prototype for generating operational control checklists "
    "based on AI system type."
)

st.markdown(
    """
    This tool helps translate AI governance concerns into practical control requirements
    across areas such as data governance, transparency, human oversight, documentation,
    monitoring, vendor risk and IP/data use.
    """
)


st.sidebar.title("AI Governance Checklist Generator")
st.sidebar.markdown(
    """
    **Prototype type:** AI Governance / LegalTech / RegTech  
    **Focus:** operational governance controls for AI systems  
    **Version:** v0.2
    """
)

st.sidebar.markdown("---")

st.sidebar.warning(
    "Public demo only. Do not enter confidential, personal or sensitive information."
)


st.subheader("1. Select AI System Type")

selected_system_type = st.selectbox(
    "Choose the type of AI system to review:",
    AI_SYSTEM_TYPES
)

if st.button("Generate governance checklist"):
    checklist = generate_checklist(selected_system_type)

    high_count, medium_count, low_count = calculate_risk_counts(checklist)
    governance_score = calculate_governance_score(checklist)
    overall_assessment = get_overall_governance_assessment(high_count, medium_count)

    st.success("Governance checklist generated.")

    st.subheader("2. Governance Risk Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Controls generated", len(checklist))
    col2.metric("High-risk controls", high_count)
    col3.metric("Medium-risk controls", medium_count)
    col4.metric("Governance score", governance_score)

    st.markdown(f"**Overall assessment:** {overall_assessment}")

    st.subheader("3. Governance Checklist")

    checklist_rows = []

    for control in checklist:
        checklist_rows.append({
            "Category": control["category"],
            "Risk Level": control["risk_level"],
            "Priority": control["priority"],
            "Owner": control["owner"],
            "Control Objective": control["control_objective"],
            "Recommended Control": control["recommended_control"]
        })

    checklist_df = pd.DataFrame(checklist_rows)

    st.dataframe(checklist_df, use_container_width=True)

    st.subheader("4. Detailed Controls")

    for index, control in enumerate(checklist, start=1):
        with st.expander(f"{index}. {control['category']} — {control['risk_level']}"):
            st.markdown(f"**Control Objective:** {control['control_objective']}")
            st.markdown(f"**Recommended Control:** {control['recommended_control']}")
            st.markdown(f"**Risk Level:** {control['risk_level']}")
            st.markdown(f"**Owner:** {control['owner']}")
            st.markdown(f"**Priority:** {control['priority']}")