import streamlit as st
import pandas as pd

from governance_data import AI_SYSTEM_TYPES
from checklist_engine import (
    generate_checklist,
    calculate_risk_counts,
    calculate_governance_score,
    get_overall_governance_assessment,
    get_governance_maturity_level,
    get_action_plan_recommendations
)
from report_generator import generate_markdown_report
from export import convert_markdown_to_docx_bytes

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

st.subheader("1.1 AI System Metadata")

with st.expander("Add AI system metadata", expanded=True):
    ai_system_name = st.text_input(
        "AI system name",
        placeholder="Example: Clinical decision support prototype"
    )

    business_unit = st.text_input(
        "Business unit / department",
        placeholder="Example: R&D, Legal, Product, HR, Compliance"
    )

    intended_use = st.text_area(
        "Intended use",
        placeholder="Describe how the AI system is expected to be used."
    )

    deployment_stage = st.selectbox(
        "Deployment stage",
        [
            "Idea / concept",
            "Prototype",
            "Internal testing",
            "Pilot",
            "Production",
            "Post-deployment monitoring"
        ]
    )

    data_sensitivity = st.selectbox(
        "Data sensitivity",
        [
            "Low",
            "Medium",
            "High",
            "Sensitive personal data",
            "Confidential business data"
        ]
    )

    provider_type = st.selectbox(
        "Provider type",
        [
            "Internal model",
            "External provider",
            "Open-source model",
            "Hybrid / multiple providers",
            "Not determined"
        ]
    )

    reviewer_name = st.text_input(
        "Reviewer name",
        placeholder="Example: Hugo Choiral"
    )

    review_date = st.date_input("Review date")

system_metadata = {
    "AI system name": ai_system_name,
    "Business unit": business_unit,
    "Intended use": intended_use,
    "Deployment stage": deployment_stage,
    "Data sensitivity": data_sensitivity,
    "Provider type": provider_type,
    "Reviewer name": reviewer_name,
    "Review date": str(review_date)
}

if "checklist_generated" not in st.session_state:
    st.session_state.checklist_generated = False

if "selected_system_type" not in st.session_state:
    st.session_state.selected_system_type = selected_system_type

if "system_metadata" not in st.session_state:
    st.session_state.system_metadata = system_metadata

if st.button("Generate governance checklist"):
    st.session_state.checklist_generated = True
    st.session_state.selected_system_type = selected_system_type
    st.session_state.system_metadata = system_metadata

if st.session_state.checklist_generated:
    checklist = generate_checklist(st.session_state.selected_system_type)

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

    st.subheader("3. Governance Checklist with Implementation Status")

    checklist_rows = []

    for index, control in enumerate(checklist, start=1):
        implementation_status = st.selectbox(
            label=f"Implementation status for control {index}: {control['category']}",
            options=[
                "Not Started",
                "In Progress",
                "Implemented",
                "Not Applicable"
            ],
            key=f"status_{index}_{st.session_state.selected_system_type}"
        )

        checklist_rows.append({
            "Category": control["category"],
            "Risk Level": control["risk_level"],
            "Priority": control["priority"],
            "Owner": control["owner"],
            "Implementation Status": implementation_status,
            "Control Objective": control["control_objective"],
            "Recommended Control": control["recommended_control"]
        })

    checklist_df = pd.DataFrame(checklist_rows)

    st.dataframe(checklist_df, use_container_width=True)

    st.subheader("4. Implementation Progress Overview")

    implemented_count = checklist_df[
        checklist_df["Implementation Status"] == "Implemented"
    ].shape[0]

    in_progress_count = checklist_df[
        checklist_df["Implementation Status"] == "In Progress"
    ].shape[0]

    not_started_count = checklist_df[
        checklist_df["Implementation Status"] == "Not Started"
    ].shape[0]

    not_applicable_count = checklist_df[
        checklist_df["Implementation Status"] == "Not Applicable"
    ].shape[0]

    applicable_controls_count = len(checklist_df) - not_applicable_count

    if applicable_controls_count > 0:
        implementation_completion_rate = round(
            implemented_count / applicable_controls_count * 100,
            1
        )
    else:
        implementation_completion_rate = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Implemented", implemented_count)
    col2.metric("In Progress", in_progress_count)
    col3.metric("Not Started", not_started_count)
    col4.metric("Completion Rate", f"{implementation_completion_rate}%")

    governance_maturity_level = get_governance_maturity_level(
        implementation_completion_rate
    )

    st.markdown(f"**Governance maturity level:** {governance_maturity_level}")

    action_plan_recommendations = get_action_plan_recommendations(
        governance_maturity_level
    )

    st.markdown("**Recommended action plan:**")

    for recommendation in action_plan_recommendations:
        st.markdown(f"- {recommendation}")

    st.subheader("5. Detailed Controls")

    for index, control in enumerate(checklist, start=1):
        with st.expander(f"{index}. {control['category']} — {control['risk_level']}"):
            st.markdown(f"**Control Objective:** {control['control_objective']}")
            st.markdown(f"**Recommended Control:** {control['recommended_control']}")
            st.markdown(f"**Risk Level:** {control['risk_level']}")
            st.markdown(f"**Owner:** {control['owner']}")
            st.markdown(f"**Priority:** {control['priority']}")

    st.subheader("6. Governance Report")

    report = generate_markdown_report(
        st.session_state.selected_system_type,
        checklist,
        checklist_df,
        st.session_state.system_metadata
    )

    st.markdown(report)

    st.download_button(
        label="Download governance report as Markdown",
        data=report,
        file_name="ai_governance_checklist_report.md",
        mime="text/markdown"
    )

    docx_report = convert_markdown_to_docx_bytes(report)

    st.download_button(
       label="Download governance report as DOCX",
       data=docx_report,
       file_name="ai_governance_checklist_report.docx",
     mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )