import streamlit as st
import pandas as pd

from governance_data import AI_SYSTEM_TYPES
from checklist_engine import (
    generate_checklist,
    calculate_risk_counts,
    calculate_governance_score,
    get_overall_governance_assessment,
    get_governance_maturity_level,
    get_action_plan_recommendations,
    identify_governance_gap
)
from report_generator import generate_markdown_report
from export import convert_markdown_to_docx_bytes

st.set_page_config(
    page_title="AI Governance Checklist Generator",
    layout="wide"
)


st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">LegalTech / RegTech Prototype</div>
        <h1>AI Governance Checklist Generator</h1>
        <p class="small-muted">
            Enterprise-style prototype for AI governance reviews, maturity assessment,
            gap analysis, risk register generation and exportable governance reports.
        </p>
        <div>
            <span class="pill">AI Governance</span>
            <span class="pill">Risk Register</span>
            <span class="pill">Maturity Assessment</span>
            <span class="pill">DOCX / CSV Export</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    h1 {
        letter-spacing: -0.04em;
        color: #0F172A;
        font-weight: 750;
    }

    h2, h3 {
        color: #0F172A;
        letter-spacing: -0.02em;
    }

    .hero-card {
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 26px 30px;
        margin-bottom: 14px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    }

    .section-card {
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 22px 24px;
        margin-top: 12px;
        margin-bottom: 18px;
        background-color: #FFFFFF;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.045);
    }

    .eyebrow {
        color: #2563EB;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .small-muted {
        color: #64748B;
        font-size: 0.95rem;
        line-height: 1.55;
    }

    .pill {
        display: inline-block;
        padding: 6px 12px;
        margin-right: 6px;
        margin-bottom: 6px;
        border-radius: 999px;
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #1D4ED8;
        font-size: 0.84rem;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetric"] label {
        color: #64748B;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #0F172A;
        font-weight: 750;
    }

    .section-divider {
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
        border-top: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("AI Governance")

st.sidebar.markdown(
    """
    **Type:** LegalTech / RegTech  
    **Mode:** Governance review  
    **Version:** v1.1
    """
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Core outputs")

st.sidebar.markdown(
    """
    - Governance checklist
    - Gap analysis
    - Risk register
    - Maturity assessment
    - DOCX / CSV exports
    """
)

st.sidebar.markdown("---")

st.sidebar.warning(
    "Public demo. Do not enter confidential or sensitive information."
)

st.markdown(
    """
    <div class="section-card">
        <div class="eyebrow">Review Workspace</div>
        <h2 style="margin-top: 0.2rem; margin-bottom: 0.4rem;">
            Configure the AI governance review
        </h2>
        <p class="small-muted" style="margin-bottom: 0;">
            Select the system type, add metadata and generate a governance dashboard.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### Review Setup")

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

if st.session_state.demo_mode:
    default_ai_system_name = "Medical Imaging Triage Assistant"
    default_business_unit = "R&D / Product"
    default_intended_use = (
        "Support internal testing of image triage recommendations for medical imaging workflows."
    )
    default_deployment_stage = "Prototype"
    default_data_sensitivity = "Sensitive personal data"
    default_provider_type = "Internal model"
    default_reviewer_name = "Hugo Choiral"
else:
    default_ai_system_name = ""
    default_business_unit = ""
    default_intended_use = ""
    default_deployment_stage = "Idea / concept"
    default_data_sensitivity = "Low"
    default_provider_type = "Not determined"
    default_reviewer_name = ""

setup_col1, setup_col2 = st.columns([1, 2])

with setup_col1:
    st.markdown("#### AI System Classification")
    if st.button("Load sample medical AI review", use_container_width=True):
        st.session_state.demo_mode = True

    selected_system_type = st.selectbox(
        "Choose the type of AI system to review:",
        AI_SYSTEM_TYPES,
        index=AI_SYSTEM_TYPES.index("Medical AI system") if st.session_state.demo_mode else 0
    )

    st.markdown(
        """
        <div class="small-muted" style="margin-top: 0.75rem;">
        Determines the baseline control library, risk scoring and recommended governance review areas.
        </div>
        """,
        unsafe_allow_html=True
    )

with setup_col2:
    st.markdown("#### AI System Metadata")

    with st.expander("Add AI system metadata", expanded=True):
        ai_system_name = st.text_input(
            "AI system name",
            value=default_ai_system_name,
            placeholder="Example: Clinical decision support prototype"
        )

        business_unit = st.text_input(
            "Business unit / department",
            value=default_business_unit,
            placeholder="Example: R&D, Legal, Product, HR, Compliance"
        )

        intended_use = st.text_area(
            "Intended use",
            value=default_intended_use,
            placeholder="Describe how the AI system is expected to be used."
        )

        deployment_stage_options = [
            "Idea / concept",
            "Prototype",
            "Internal testing",
            "Pilot",
            "Production",
            "Post-deployment monitoring"
        ]

        deployment_stage = st.selectbox(
            "Deployment stage",
            deployment_stage_options,
            index=deployment_stage_options.index(default_deployment_stage)
        )

        data_sensitivity_options = [
            "Low",
            "Medium",
            "High",
            "Sensitive personal data",
            "Confidential business data"
        ]

        data_sensitivity = st.selectbox(
            "Data sensitivity",
            data_sensitivity_options,
            index=data_sensitivity_options.index(default_data_sensitivity)
        )

        provider_type_options = [
            "Internal model",
            "External provider",
            "Open-source model",
            "Hybrid / multiple providers",
            "Not determined"
        ]

        provider_type = st.selectbox(
            "Provider type",
            provider_type_options,
            index=provider_type_options.index(default_provider_type)
        )

        reviewer_name = st.text_input(
            "Reviewer name",
            value=default_reviewer_name,
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

if st.button("Generate AI governance review"):
    st.session_state.checklist_generated = True
    st.session_state.selected_system_type = selected_system_type
    st.session_state.system_metadata = system_metadata

if st.session_state.checklist_generated:
    checklist = generate_checklist(st.session_state.selected_system_type)

    high_count, medium_count, low_count = calculate_risk_counts(checklist)
    governance_score = calculate_governance_score(checklist)
    overall_assessment = get_overall_governance_assessment(high_count, medium_count)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.success("AI governance review generated successfully.")

    st.markdown(
        f"""
        <div class="section-card">
            <div class="eyebrow">GOVERNANCE REVIEW DASHBOARD</div>
            <h2 style="margin-top: 0.4rem;">{st.session_state.selected_system_type}</h2>
            <p class="small-muted">
                Review generated from the selected AI system profile. Use the dashboard below
                to assess risk exposure, implementation status, governance gaps and exportable outputs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Governance Risk Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Controls generated", len(checklist))
    col2.metric("High-risk controls", high_count)
    col3.metric("Medium-risk controls", medium_count)
    col4.metric("Governance score", governance_score)

    st.markdown(f"**Overall assessment:** {overall_assessment}")

    st.subheader("Control Implementation Tracker")

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

        governance_gap = identify_governance_gap(control, implementation_status)

        checklist_rows.append({
            "Category": control["category"],
            "Risk Level": control["risk_level"],
            "Priority": control["priority"],
            "Owner": control["owner"],
            "Implementation Status": implementation_status,
            "Governance Gap": governance_gap,
            "Control Objective": control["control_objective"],
            "Recommended Control": control["recommended_control"]
        })

    checklist_df = pd.DataFrame(checklist_rows)

    st.markdown("### Filter governance controls")

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    risk_level_filter = filter_col1.multiselect(
        "Filter by risk level",
        options=sorted(checklist_df["Risk Level"].unique()),
        default=sorted(checklist_df["Risk Level"].unique())
    )

    priority_filter = filter_col2.multiselect(
        "Filter by priority",
        options=sorted(checklist_df["Priority"].unique()),
        default=sorted(checklist_df["Priority"].unique())
    )

    status_filter = filter_col3.multiselect(
        "Filter by implementation status",
        options=sorted(checklist_df["Implementation Status"].unique()),
        default=sorted(checklist_df["Implementation Status"].unique())
    )

    owner_filter = filter_col4.multiselect(
        "Filter by owner",
        options=sorted(checklist_df["Owner"].unique()),
        default=sorted(checklist_df["Owner"].unique())
    )

    filtered_checklist_df = checklist_df[
        checklist_df["Risk Level"].isin(risk_level_filter)
        & checklist_df["Priority"].isin(priority_filter)
        & checklist_df["Implementation Status"].isin(status_filter)
        & checklist_df["Owner"].isin(owner_filter)
    ]

    st.dataframe(filtered_checklist_df, use_container_width=True)

    st.caption(
        f"Showing {len(filtered_checklist_df)} of {len(checklist_df)} governance controls."
    )

    st.subheader("Governance Gap Analysis")

    gap_counts = checklist_df["Governance Gap"].value_counts()

    for gap_label, gap_count in gap_counts.items():
        st.markdown(f"- **{gap_label}:** {gap_count}")

    critical_gap_count = checklist_df[
        checklist_df["Governance Gap"] == "Critical governance gap"
    ].shape[0]

    immediate_action_count = checklist_df[
        checklist_df["Governance Gap"] == "Immediate action required"
    ].shape[0]

    if critical_gap_count > 0 or immediate_action_count > 0:
        st.error(
            "Critical governance gaps or immediate action items were identified. "
            "These should be addressed before deployment, external use or scaling."
        )
    else:
        st.success(
            "No critical governance gaps identified based on the current implementation status."
        )

    st.subheader("AI Governance Risk Register")

    risk_register_rows = []

    for index, row in checklist_df.iterrows():
        risk_register_rows.append({
            "Risk ID": f"AI-GOV-{index + 1:03d}",
            "Category": row["Category"],
            "Risk Level": row["Risk Level"],
            "Priority": row["Priority"],
            "Owner": row["Owner"],
            "Implementation Status": row["Implementation Status"],
            "Governance Gap": row["Governance Gap"],
            "Recommended Control": row["Recommended Control"]
        })

    risk_register_df = pd.DataFrame(risk_register_rows)

    risk_register_csv = risk_register_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download risk register as CSV",
        data=risk_register_csv,
        file_name="ai_governance_risk_register.csv",
        mime="text/csv"
    )

    st.dataframe(risk_register_df, use_container_width=True)

    st.subheader("Implementation Progress & Maturity")

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

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-card">
            <div class="eyebrow">Control Library</div>
            <h2 style="margin-top: 0.4rem;">Detailed governance controls</h2>
            <p class="small-muted">
                Expand each control to review the control objective, recommended implementation,
                owner, risk level and priority.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    for index, control in enumerate(checklist, start=1):
        with st.expander(f"{index}. {control['category']} — {control['risk_level']}"):
            st.markdown(f"**Control Objective:** {control['control_objective']}")
            st.markdown(f"**Recommended Control:** {control['recommended_control']}")
            st.markdown(f"**Risk Level:** {control['risk_level']}")
            st.markdown(f"**Owner:** {control['owner']}")
            st.markdown(f"**Priority:** {control['priority']}")

    st.subheader("Export Center")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-card">
            <div class="eyebrow">Export Center</div>
            <h2 style="margin-top: 0.4rem;">Generate governance deliverables</h2>
            <p class="small-muted">
                Export the governance review as Markdown, DOCX or CSV for internal documentation,
                compliance tracking, risk register management or portfolio demonstration.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    export_col1, export_col2 = st.columns([2, 1])

    with export_col1:
        st.markdown(
            """
            **Available exports**

            - Markdown governance report
            - DOCX governance report
            - CSV AI governance risk register
            """
        )

    with export_col2:
        st.markdown(
            """
            **Typical use**

            Internal review, compliance tracking, management reporting and portfolio demonstration.
            """
        )

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