from checklist_engine import (
    calculate_risk_counts,
    calculate_governance_score,
    get_overall_governance_assessment,
    get_governance_maturity_level,
    get_action_plan_recommendations
)


def generate_markdown_report(
    ai_system_type,
    checklist,
    checklist_df=None,
    system_metadata=None
):
    high_count, medium_count, low_count = calculate_risk_counts(checklist)
    governance_score = calculate_governance_score(checklist)
    overall_assessment = get_overall_governance_assessment(high_count, medium_count)

    report = "# AI Governance Checklist Report\n\n"

    report += "## Executive Summary\n\n"
    report += f"- **AI system type:** {ai_system_type}\n"
    report += f"- **Total controls generated:** {len(checklist)}\n"
    report += f"- **High-risk controls:** {high_count}\n"
    report += f"- **Medium-risk controls:** {medium_count}\n"
    report += f"- **Low-risk controls:** {low_count}\n"
    report += f"- **Governance score:** {governance_score}\n"
    report += f"- **Overall assessment:** {overall_assessment}\n\n"
        
    if system_metadata:
        report += "## AI System Metadata\n\n"

        for key, value in system_metadata.items():
            if value:
                report += f"- **{key}:** {value}\n"

        report += "\n"

    if checklist_df is not None and "Implementation Status" in checklist_df.columns:
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

        report += "## Implementation Progress Overview\n\n"
        report += f"- **Implemented controls:** {implemented_count}\n"
        report += f"- **Controls in progress:** {in_progress_count}\n"
        report += f"- **Controls not started:** {not_started_count}\n"
        report += f"- **Controls not applicable:** {not_applicable_count}\n"
        governance_maturity_level = get_governance_maturity_level(
              implementation_completion_rate
        )

        report += f"- **Implementation completion rate:** {implementation_completion_rate}%\n"
        report += f"- **Governance maturity level:** {governance_maturity_level}\n\n"
        action_plan_recommendations = get_action_plan_recommendations(
            governance_maturity_level
        )

        report += "## Recommended Action Plan\n\n"

        for recommendation in action_plan_recommendations:
            report += f"- {recommendation}\n"

        report += "\n"

    report += "## Governance Risk Overview\n\n"
    report += (
        "This section summarizes the governance attention required for the selected AI system type. "
        "Higher scores indicate that stronger governance controls, documentation, review mechanisms "
        "and internal accountability measures should be implemented before deployment or operational use.\n\n"
    )

    report += "## Governance Checklist\n\n"

    if checklist_df is not None and "Implementation Status" in checklist_df.columns:
        report += "| Category | Risk Level | Priority | Owner | Implementation Status |\n"
        report += "|---|---|---|---|---|\n"

        for _, row in checklist_df.iterrows():
            report += (
                f"| {row['Category']} | "
                f"{row['Risk Level']} | "
                f"{row['Priority']} | "
                f"{row['Owner']} | "
                f"{row['Implementation Status']} |\n"
            )
    else:
        report += "| Category | Risk Level | Priority | Owner |\n"
        report += "|---|---|---|---|\n"

        for control in checklist:
            report += (
                f"| {control['category']} | "
                f"{control['risk_level']} | "
                f"{control['priority']} | "
                f"{control['owner']} |\n"
            )

    report += "\n"

    report += "## Detailed Recommended Controls\n\n"

    for index, control in enumerate(checklist, start=1):
        implementation_status = "Not specified"

        if checklist_df is not None and "Implementation Status" in checklist_df.columns:
            implementation_status = checklist_df.iloc[index - 1]["Implementation Status"]

        report += f"### Control {index}: {control['category']}\n\n"
        report += f"- **Risk Level:** {control['risk_level']}\n"
        report += f"- **Priority:** {control['priority']}\n"
        report += f"- **Owner:** {control['owner']}\n"
        report += f"- **Implementation Status:** {implementation_status}\n"
        report += f"- **Control Objective:** {control['control_objective']}\n"
        report += f"- **Recommended Control:** {control['recommended_control']}\n\n"

    report += "## Strategic Use\n\n"
    report += (
        "This report can support early-stage AI governance review by helping legal, compliance, "
        "product, data and business teams identify key control areas before deploying or scaling "
        "an AI system. It is designed as an operational checklist rather than a formal regulatory "
        "compliance certification.\n\n"
    )

    report += "## Disclaimer\n\n"
    report += (
        "This report is generated by a rule-based prototype for educational and portfolio purposes only. "
        "It does not provide legal advice, regulatory advice or compliance certification. "
        "Users should consult qualified professionals before making legal, regulatory or business decisions.\n"
    )

    return report